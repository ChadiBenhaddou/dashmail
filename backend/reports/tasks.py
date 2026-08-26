import os

import openai
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3, retry_backoff=True)
def process_report(self, report_id):
    from django.utils import timezone as dj_timezone

    from .models import Report
    from .services.chart_generator import generate_charts_config
    from .services.data_cleaner import clean_data
    from .services.data_parser import parse_file
    from .services.email_notifier import send_failure_email, send_success_email
    from .services.error_handler import (
        FileCorruptedError,
        FileFormatError,
        LLMFormatError,
        LLMTimeoutError,
        NoColumnsError,
        handle_pipeline_error,
    )
    from .services.llm_prompt import SCHEMA_INSTRUCTIONS, SYSTEM_PROMPT, build_analysis_prompt
    from .services.llm_service import call_llm

    try:
        report = Report.objects.get(id=report_id)
    except Report.DoesNotExist:
        logger.error("Report %s not found", report_id)
        return {"error": "Report not found"}

    try:
        # 1. Load report + data_file
        report.status = Report.Status.PARSING
        report.save(update_fields=["status"])

        data_file = report.data_file
        file_path = data_file.file.path

        if not os.path.exists(file_path):
            raise FileCorruptedError(detail="Le fichier est introuvable sur le serveur")

        file_size = os.path.getsize(file_path)
        report.file_size = file_size
        report.save(update_fields=["file_size"])

        # 2. Parse CSV/Excel
        try:
            parse_result = parse_file(file_path)
        except ValueError as exc:
            msg = str(exc).lower()
            if "unsupported" in msg or "format" in msg:
                raise FileFormatError(detail=str(exc)) from exc
            if "empty" in msg or "no data" in msg:
                raise NoColumnsError() from exc
            raise FileCorruptedError(detail=str(exc)) from exc
        except Exception as exc:
            raise FileCorruptedError(detail=str(exc)) from exc

        import pandas as pd

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            df = None
            for enc in ("utf-8", "latin-1"):
                try:
                    df = pd.read_csv(file_path, encoding=enc)
                    break
                except UnicodeDecodeError:
                    continue
            if df is None:
                raise FileCorruptedError(detail="Impossible de lire le fichier CSV avec les encodages supportés")
        else:
            try:
                df = pd.read_excel(file_path)
            except Exception as exc:
                raise FileCorruptedError(detail=str(exc)) from exc

        if df is None or df.empty:
            raise NoColumnsError()

        report.row_count = parse_result["row_count"]
        report.column_count = parse_result["column_count"]
        report.save(update_fields=["row_count", "column_count"])

        # 3. Clean data
        report.status = Report.Status.ANALYZING
        report.save(update_fields=["status"])

        cleaned_df, cleaning_log = clean_data(df)
        report.cleaning_log = cleaning_log

        missing_pct = parse_result.get("missing_pct", 0)
        dup_pct = 0
        if parse_result["row_count"] > 0:
            dup_pct = (parse_result["duplicate_rows"] / parse_result["row_count"]) * 100
        quality_score = max(0.0, round(100 - missing_pct - dup_pct, 1))
        report.data_quality_score = quality_score
        report.save(update_fields=["cleaning_log", "data_quality_score"])

        # 4. Build LLM prompt
        system_prompt, user_prompt = build_analysis_prompt(parse_result)

        # 5. Call LLM
        try:
            llm_response = call_llm(system_prompt, user_prompt)
        except openai.APITimeoutError:
            raise LLMTimeoutError()
        except openai.APIStatusError as exc:
            if exc.status_code >= 500:
                raise LLMTimeoutError() from exc
            raise FileCorruptedError(detail=f"Erreur API LLM: {exc.status_code}") from exc
        except (ValueError, KeyError) as exc:
            raise LLMFormatError(detail=str(exc)) from exc

        report.llm_insights = llm_response

        # 6. Generate Recharts JSON
        report.status = Report.Status.GENERATING
        report.save(update_fields=["status"])

        charts_config = generate_charts_config(cleaned_df, llm_response)
        report.charts_config = charts_config

        # 7. Save everything
        report.status = Report.Status.COMPLETED
        report.processed_at = dj_timezone.now()
        report.save(update_fields=[
            "status", "processed_at", "charts_config", "llm_insights",
        ])

        logger.info("Report %s processed successfully", report_id)

        send_success_email(report)

        return {"status": "completed", "report_id": str(report_id)}

    except Exception as exc:
        handle_pipeline_error(exc, report)
        logger.exception("Failed to process report %s", report_id)

        send_failure_email(report)

        if not isinstance(exc, (FileFormatError, FileCorruptedError, NoColumnsError)):
            raise self.retry(exc=exc)
        return {"status": "failed", "report_id": str(report_id)}
