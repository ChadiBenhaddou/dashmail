import pandas as pd

DEFAULT_KPI_LIMIT = 4


def compute_kpis(cleaned_df, kpi_config):
    """Compute real KPI values from pandas based on LLM-supplied descriptors.

    kpi_config is a list of:
        {"label": str, "x_axis": str, "y_axis": str,
         "calculation": "sum"|"mean"|"count"|"max"|"min"}
    """
    if not kpi_config or cleaned_df is None or cleaned_df.empty:
        return _fallback_kpis(cleaned_df)

    kpis = []
    for desc in kpi_config[:DEFAULT_KPI_LIMIT]:
        label = desc.get("label") or "Indicateur"
        x_axis = desc.get("x_axis", "")
        y_axis = desc.get("y_axis", "")
        calculation = (desc.get("calculation") or "sum").lower()

        if x_axis not in cleaned_df.columns:
            continue

        try:
            value, variation = _compute_single(
                cleaned_df, x_axis, y_axis, calculation
            )
        except Exception:
            continue

        if value is None:
            continue

        kpi_item = {"label": label, "value": round(value, 2)}
        if variation is not None:
            kpi_item["variation"] = round(variation, 1)
        kpis.append(kpi_item)

    if not kpis:
        return _fallback_kpis(cleaned_df)

    return kpis


def _compute_single(df, x_axis, y_axis, calculation):
    work = df.copy()

    if calculation == "count":
        value = float(len(work))
        variation = _date_variation(work, x_axis, "count")
        return value, variation

    if y_axis not in work.columns or not pd.api.types.is_numeric_dtype(work[y_axis]):
        return None, None

    series = work[y_axis].dropna()

    if calculation == "mean":
        value = float(series.mean())
    elif calculation == "max":
        value = float(series.max())
    elif calculation == "min":
        value = float(series.min())
    else:
        value = float(series.sum())

    variation = _date_variation(work, x_axis, calculation, y_axis)
    return value, variation


def _date_variation(df, x_axis, calculation, y_axis=None):
    """Compute current-vs-previous variation when x_axis is a date-like column.

    Splits the rows into two halves (recent vs earlier) and compares the metric.
    Returns None when a numeric comparison is not meaningful.
    """
    if x_axis not in df.columns:
        return None
    if not _is_date_column(df, x_axis):
        return None

    work = df.copy()
    work = work.dropna(subset=[x_axis]).sort_values(x_axis)
    if len(work) < 4:
        return None

    split = len(work) // 2
    earlier = work.iloc[:split]
    recent = work.iloc[split:]

    def metric(frame):
        if calculation == "count":
            return float(len(frame))
        if y_axis not in frame.columns or not pd.api.types.is_numeric_dtype(frame[y_axis]):
            return None
        s = frame[y_axis].dropna()
        if len(s) == 0:
            return None
        return float({"mean": s.mean(), "max": s.max(), "min": s.min()}.get(calculation, s.sum()))

    prev_v = metric(earlier)
    curr_v = metric(recent)
    if prev_v is None or curr_v is None or prev_v == 0:
        return None
    return ((curr_v - prev_v) / abs(prev_v)) * 100


def _fallback_kpis(df):
    if df is None or len(df.columns) == 0:
        return []
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cat_cols = [c for c in df.columns if df[c].dtype == "object"]

    kpis = []
    if numeric_cols:
        for col in numeric_cols[:2]:
            kpis.append({"label": f"Total {col}", "value": round(float(df[col].sum()), 2)})
            kpis.append({"label": f"Moyenne {col}", "value": round(float(df[col].mean()), 2)})
    if cat_cols:
        top = df[cat_cols[0]].value_counts().head(1)
        if len(top):
            kpis.append({"label": f"Valeur top — {cat_cols[0]}", "value": int(top.iloc[0])})

    kpis.append({"label": "Lignes", "value": len(df)})
    return kpis[:4]


def _is_date_column(df, col):
    if pd.api.types.is_datetime64_any_dtype(df[col]):
        return True
    if df[col].dtype == object or pd.api.types.is_string_dtype(df[col]):
        parsed = pd.to_datetime(df[col].dropna(), errors="coerce")
        if len(parsed) > 0 and parsed.notna().sum() >= len(parsed) * 0.5:
            return True
    return False
