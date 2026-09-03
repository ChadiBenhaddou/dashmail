import pandas as pd


def build_dashboard_profile(df):
    """Build a human-friendly profile of the dataset with real numbers.

    Used to render a "Dataset overview" panel proving content analysis.
    """
    if df is None or len(df.columns) == 0:
        return {}

    profile = {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "numeric_columns": [],
        "categorical_columns": [],
        "date_columns": [],
        "missing_total": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }

    for col in df.columns:
        series = df[col]
        is_date = _is_date_column(df, col)
        is_numeric = pd.api.types.is_numeric_dtype(series)

        if is_numeric:
            entry = {
                "name": col,
                "type": "numeric",
                "min": _round(series.min()),
                "max": _round(series.max()),
                "mean": _round(series.mean()),
                "sum": _round(series.sum()),
            }
            profile["numeric_columns"].append(entry)
        elif is_date:
            profile["date_columns"].append(col)
        else:
            counts = series.value_counts().head(5)
            top = [{"value": str(k), "count": int(v)} for k, v in counts.items()]
            profile["categorical_columns"].append(
                {"name": col, "top_values": top}
            )

    return profile


def _round(value):
    if value is None or pd.isna(value):
        return None
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(num) >= 1000 or num != int(num):
        return round(num, 2)
    return int(num)


def _is_date_column(df, col):
    if pd.api.types.is_datetime64_any_dtype(df[col]):
        return True
    if df[col].dtype == object or pd.api.types.is_string_dtype(df[col]):
        parsed = pd.to_datetime(df[col].dropna(), errors="coerce")
        if len(parsed) > 0 and parsed.notna().sum() >= len(parsed) * 0.5:
            return True
    return False
