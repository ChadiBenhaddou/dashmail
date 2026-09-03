import pandas as pd

DEFAULT_COLORS = [
    "#4F46E5", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6",
    "#EC4899", "#06B6D4", "#84CC16", "#F97316", "#6366F1",
]

MAX_CHARTS = 7


def generate_charts_config(cleaned_df, llm_response):
    visualizations = llm_response.get("visualizations", [])
    charts = [_build_chart(cleaned_df, viz, i, DEFAULT_COLORS[i % len(DEFAULT_COLORS)])
              for i, viz in enumerate(visualizations)]
    charts = [c for c in charts if c is not None]
    charts = _dedupe_pies(charts)

    for viz in llm_response.get("custom_visualizations", []):
        custom = _build_custom_chart(cleaned_df, viz)
        if custom is not None:
            charts.append(custom)

    charts = _dedupe_pies(charts)

    # Cap total charts (auto first, then custom)
    return charts[:MAX_CHARTS]


def generate_custom_chart(cleaned_df, viz):
    return _build_custom_chart(cleaned_df, viz)


def _dedupe_pies(charts):
    seen_pie = False
    result = []
    for c in charts:
        if c.get("type") == "pie":
            if seen_pie:
                continue
            seen_pie = True
        result.append(c)
    return result


def _build_chart(df, viz, idx, color):
    chart_type = viz.get("type", "bar")
    x_axis = viz.get("x_axis", "")
    y_axis = viz.get("y_axis", "")
    title = viz.get("title", f"Graphique {idx + 1}")
    calculation = viz.get("calculation")
    group = viz.get("group") or ""

    if x_axis not in df.columns:
        return None

    try:
        if chart_type == "pie":
            data = _build_pie_data(df, x_axis, y_axis, calculation)
        else:
            data = _build_data_for(df, chart_type, x_axis, y_axis, calculation, group)
    except Exception:
        return None

    if not data:
        return None

    chart = {
        "type": chart_type,
        "title": title,
        "data": data,
        "xAxisKey": x_axis,
        "yAxisKey": y_axis,
        "colors": [color],
        "description": viz.get("description", ""),
    }

    if group and group in df.columns:
        series_keys = sorted(df[group].dropna().unique().tolist())
        chart["seriesKeys"] = series_keys
        chart["group"] = group
        chart["colors"] = [DEFAULT_COLORS[i % len(DEFAULT_COLORS)] for i in range(len(series_keys))]

    return chart


def _build_custom_chart(df, viz):
    chart_type = viz.get("type", "bar")
    x_axis = viz.get("x_axis", "")
    y_axis = viz.get("y_axis", "")
    calculation = viz.get("calculation", "sum")
    title = viz.get("title", "Graphique personnalisé")
    group = viz.get("group") or ""

    if x_axis not in df.columns:
        return None

    data = _build_data_for(df, chart_type, x_axis, y_axis, calculation, group)
    if not data:
        return None

    chart = {
        "type": chart_type,
        "title": title,
        "data": data,
        "xAxisKey": x_axis,
        "yAxisKey": y_axis,
        "colors": [DEFAULT_COLORS[0]],
        "description": viz.get("description", ""),
        "custom": True,
    }

    if group and group in df.columns:
        series_keys = sorted(df[group].dropna().unique().tolist())
        chart["seriesKeys"] = series_keys
        chart["group"] = group
        chart["colors"] = [DEFAULT_COLORS[i % len(DEFAULT_COLORS)] for i in range(len(series_keys))]

    return chart


def _build_data_for(df, chart_type, x_axis, y_axis, calculation, group=""):
    if group and group in df.columns and group != x_axis and chart_type in ("line", "bar", "area"):
        return _build_grouped_data(df, x_axis, y_axis, group, calculation)

    if chart_type == "line":
        return _build_custom_data(df, x_axis, y_axis, calculation or "mean")
    if chart_type == "area":
        return _build_custom_data(df, x_axis, y_axis, calculation or "mean")
    if chart_type == "bar":
        return _build_custom_data(df, x_axis, y_axis, calculation or "sum")
    if chart_type == "scatter":
        return _build_scatter_data(df, x_axis, y_axis)
    if chart_type == "radar":
        return _build_custom_data(df, x_axis, y_axis, calculation or "mean")
    return _build_custom_data(df, x_axis, y_axis, calculation or "sum")


def _build_grouped_data(df, x_axis, y_axis, group, calculation):
    work = df.copy()
    calc = (calculation or "sum").lower()
    agg = {
        "sum": "sum",
        "mean": "mean",
        "avg": "mean",
        "max": "max",
        "min": "min",
        "count": "count",
    }.get(calc, "sum")

    if agg == "count":
        pivot = work.pivot_table(index=x_axis, columns=group, values=y_axis, aggfunc="size", fill_value=0)
    else:
        if y_axis not in work.columns or not pd.api.types.is_numeric_dtype(work[y_axis]):
            return []
        pivot = work.pivot_table(index=x_axis, columns=group, values=y_axis, aggfunc=agg, fill_value=0)

    pivot = pivot.reset_index()
    for col in pivot.columns:
        if col != x_axis and pd.api.types.is_numeric_dtype(pivot[col]):
            pivot[col] = pivot[col].round(2)
    records = pivot.to_dict(orient="records")
    # limit number of categories for readability
    return records[:30]


def _build_scatter_data(df, x_axis, y_axis):
    work = df.copy()
    if (
        x_axis not in work.columns
        or y_axis not in work.columns
        or not pd.api.types.is_numeric_dtype(work[x_axis])
        or not pd.api.types.is_numeric_dtype(work[y_axis])
    ):
        return []
    work = work[[x_axis, y_axis]].dropna()
    work[x_axis] = work[x_axis].round(2)
    work[y_axis] = work[y_axis].round(2)
    return work.to_dict(orient="records")


def _build_custom_data(df, x_axis, y_axis, calculation):
    work = df.copy()
    calculation = (calculation or "sum").lower()

    if calculation == "count":
        counts = work[x_axis].value_counts().reset_index()
        counts.columns = [x_axis, y_axis]
        return add_index(counts.to_dict(orient="records"))

    if y_axis not in work.columns or not pd.api.types.is_numeric_dtype(work[y_axis]):
        return []

    if _is_date_column(work, x_axis):
        work[x_axis] = _parse_dates(work, x_axis)
        work = work.dropna(subset=[x_axis]).sort_values(x_axis)
        work[x_axis] = work[x_axis].dt.strftime("%Y-%m-%d")

    if work[x_axis].nunique() > 30:
        top = work[x_axis].value_counts().head(15).index
        work = work[work[x_axis].isin(top)]

    agg = {
        "sum": "sum",
        "mean": "mean",
        "avg": "mean",
        "max": "max",
        "min": "min",
    }.get(calculation, "sum")
    grouped = work.groupby(x_axis, sort=True)[y_axis].agg(agg).reset_index()
    grouped[y_axis] = grouped[y_axis].round(2)
    if agg == "sum":
        grouped = grouped.sort_values(y_axis, ascending=False)
    return add_index(grouped.to_dict(orient="records"))


def add_index(records):
    for i, rec in enumerate(records):
        rec.setdefault("_index", i)
    return records


def _is_date_column(df, col):
    if pd.api.types.is_datetime64_any_dtype(df[col]):
        return True
    if df[col].dtype == object or pd.api.types.is_string_dtype(df[col]):
        parsed = pd.to_datetime(df[col].dropna(), errors="coerce")
        if len(parsed) > 0 and parsed.notna().sum() >= len(parsed) * 0.5:
            return True
    return False


def _parse_dates(df, col):
    return pd.to_datetime(df[col], errors="coerce")


def _build_line_data(df, x_axis, y_axis):
    return _build_custom_data(df, x_axis, y_axis, "mean")


def _build_pie_data(df, x_axis, y_axis, calculation=None):
    work = df.copy()

    if y_axis in work.columns and pd.api.types.is_numeric_dtype(work[y_axis]):
        grouped = work.groupby(x_axis)[y_axis].sum().reset_index()
    else:
        counts = work[x_axis].value_counts().reset_index()
        counts.columns = [x_axis, y_axis]
        grouped = counts

    grouped[y_axis] = grouped[y_axis].round(2)
    grouped = grouped.sort_values(y_axis, ascending=False).head(10)
    return add_index(grouped.to_dict(orient="records"))
