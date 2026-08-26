import email
import imaplib
import logging
import os
import tempfile
from email.header import decode_header

from django.conf import settings

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
MAX_ATTACHMENT_SIZE = 50 * 1024 * 1024  # 50 MB


def _decode_header_value(value):
    if value is None:
        return ""
    decoded_parts = decode_header(value)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)


def _get_email_config():
    return {
        "host": os.environ.get("EMAIL_IMAP_HOST", ""),
        "port": int(os.environ.get("EMAIL_IMAP_PORT", "993")),
        "user": os.environ.get("EMAIL_IMAP_USER", ""),
        "password": os.environ.get("EMAIL_IMAP_PASSWORD", ""),
    }


def _is_valid_attachment(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def check_email_inbox():
    from reports.models import DataFile, Report

    config = _get_email_config()

    if not all([config["host"], config["user"], config["password"]]):
        logger.warning("IMAP configuration incomplete, skipping email check")
        return {"processed": 0, "errors": []}

    processed_count = 0
    errors = []

    try:
        mail = imaplib.IMAP4_SSL(config["host"], config["port"])
        mail.login(config["user"], config["password"])
        mail.select("INBOX")

        _, message_ids = mail.search(None, "UNSEEN")

        if not message_ids[0]:
            logger.info("No unseen emails in inbox")
            mail.logout()
            return {"processed": 0, "errors": []}

        id_list = message_ids[0].split()

        for msg_id in id_list:
            try:
                _, msg_data = mail.fetch(msg_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = _decode_header_value(msg.get("Subject", ""))
                sender = msg.get("From", "")

                has_valid_attachment = False

                for part in msg.walk():
                    content_disposition = str(part.get("Content-Disposition", ""))

                    if "attachment" not in content_disposition:
                        continue

                    filename = part.get_filename()
                    if filename:
                        filename = _decode_header_value(filename)
                    else:
                        continue

                    if not _is_valid_attachment(filename):
                        logger.info("Skipping unsupported attachment: %s", filename)
                        continue

                    payload = part.get_payload(decode=True)
                    if payload is None:
                        continue

                    if len(payload) > MAX_ATTACHMENT_SIZE:
                        logger.warning(
                            "Attachment %s exceeds size limit (%d bytes)",
                            filename,
                            len(payload),
                        )
                        errors.append(
                            {
                                "email": sender,
                                "error": f"Attachment {filename} exceeds size limit",
                            }
                        )
                        continue

                    ext = os.path.splitext(filename)[1].lower()

                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=ext
                    ) as tmp:
                        tmp.write(payload)
                        tmp_path = tmp.name

                    report_title = (
                        f"{subject} - {filename}" if subject else filename
                    )

                    report = Report.objects.create(
                        title=report_title,
                        source_file="",
                        status=Report.Status.PENDING,
                        sender_email=sender,
                        file_size=len(payload),
                    )

                    with open(tmp_path, "rb") as f:
                        report.source_file.save(filename, f, save=True)

                    data_file = DataFile.objects.create(
                        report=report,
                        file=report.source_file,
                        original_filename=filename,
                        file_type=ext.lstrip("."),
                        parsing_status=DataFile.ParsingStatus.RECEIVED,
                    )

                    try:
                        from reports.tasks import process_report

                        process_report.delay(str(report.id))
                    except Exception as task_exc:
                        logger.exception(
                            "Failed to dispatch processing task for report %s",
                            report.id,
                        )
                        report.status = Report.Status.FAILED
                        report.error_message = (
                            f"Task dispatch failed: {task_exc}"
                        )
                        report.save(
                            update_fields=["status", "error_message"]
                        )

                    try:
                        os.unlink(tmp_path)
                    except OSError:
                        pass

                    has_valid_attachment = True
                    processed_count += 1
                    logger.info(
                        "Processed attachment %s from %s (report %s)",
                        filename,
                        sender,
                        report.id,
                    )

                if has_valid_attachment:
                    mail.store(msg_id, "+FLAGS", "\\Seen")

            except Exception as exc:
                logger.exception("Error processing email %s", msg_id)
                errors.append({"email_id": msg_id, "error": str(exc)})

        mail.logout()

    except imaplib.IMAP4.error as exc:
        logger.exception("IMAP connection error")
        errors.append({"error": f"IMAP error: {exc}"})
    except Exception as exc:
        logger.exception("Unexpected error during email ingestion")
        errors.append({"error": str(exc)})

    return {"processed": processed_count, "errors": errors}
