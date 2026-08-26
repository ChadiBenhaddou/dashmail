import os

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def _detect_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {ext}")
    return {
        ".csv": "csv",
        ".xlsx": "xlsx",
        ".xls": "xls",
    }[ext]


def _read_csv(file_path):
    for encoding in ("utf-8", "latin-1"):
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to read CSV with utf-8 or latin-1 encoding")


def _read_excel(file_path):
    return pd.read_excel(file_path)


def _classify_column(series):
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    return "categorical"


def _detect_date_columns(df):
    date_cols = []
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_cols.append(col)
            continue
        if df[col].dtype == object:
            try:
                parsed = pd.to_datetime(df[col].dropna(), errors="raise")
                if len(parsed) > 0:
                    date_cols.append(col)
            except (ValueError, TypeError):
                pass
    return date_cols


def _column_summary(name, series):
    total = len(series)
    null_count = int(series.isna().sum())
    null_pct = round((null_count / total) * 100, 2) if total > 0 else 0.0
    dtype = str(series.dtype)
    sample = series.dropna().head(5).tolist()
    sample = [str(v) for v in sample]

    return {
        "name": name,
        "dtype": dtype,
        "nullable_count": null_count,
        "nullable_pct": null_pct,
        "sample_values": sample,
    }


def parse_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_type = _detect_file_type(file_path)

    if file_type == "csv":
        df = _read_csv(file_path)
    else:
        df = _read_excel(file_path)

    if df.empty:
        raise ValueError("File is empty or contains no data rows")

    rows, cols = df.shape

    columns = [_column_summary(col, df[col]) for col in df.columns]

    date_columns = _detect_date_columns(df)

    numeric_columns = [
        col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])
    ]

    categorical_columns = [
        col
        for col in df.columns
        if col not in numeric_columns and col not in date_columns
    ]

    missing_total = int(df.isna().sum().sum())
    cell_count = rows * cols if cols > 0 else 1
    missing_pct = round((missing_total / cell_count) * 100, 2)

    duplicate_rows = int(df.duplicated().sum())

    return {
        "row_count": rows,
        "column_count": cols,
        "columns": columns,
        "file_type": file_type,
        "date_columns": date_columns,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "missing_total": missing_total,
        "missing_pct": missing_pct,
        "duplicate_rows": duplicate_rows,
    }
