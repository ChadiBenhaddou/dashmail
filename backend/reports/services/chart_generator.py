import pandas as pd

DEFAULT_COLORS = [
    "#4F46E5", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6",
    "#EC4899", "#06B6D4", "#84CC16", "#F97316", "#6366F1",
]


def generate_charts_config(cleaned_df, llm_response):
    visualizations = llm_response.get("visualizations", [])
    charts = []

    for idx, viz in enumerate(visualizations):
        chart_type = viz.get("type", "bar")
        x_axis = viz.get("x_axis", "")
        y_axis = viz.get("y_axis", "")
        title = viz.get("title", f"Graphique {idx + 1}")
        colors = [DEFAULT_COLORS[idx % len(DEFAULT_COLORS)]]

        if x_axis not in cleaned_df.columns:
            continue

        try:
            if chart_type == "line":
                data = _build_line_data(cleaned_df, x_axis, y_axis)
            elif chart_type == "pie":
                data = _build_pie_data(cleaned_df, x_axis, y_axis)
            else:
                data = _build_bar_data(cleaned_df, x_axis, y_axis)
        except Exception:
            continue

        if not data:
            continue

        charts.append({
            "type": chart_type,
            "title": title,
            "data": data,
            "xAxisKey": x_axis,
            "yAxisKey": y_axis,
            "colors": colors,
            "description": viz.get("description", ""),
        })

    return charts


def _is_date_column(df, col):
    if pd.api.types.is_datetime64_any_dtype(df[col]):
        return True
    if df[col].dtype == object:
        try:
            parsed = pd.to_datetime(df[col].dropna(), errors="raise")
            return len(parsed) > 0
        except (ValueError, TypeError):
            pass
    return False


def _parse_dates(df, col):
    return pd.to_datetime(df[col], errors="coerce")


def _build_line_data(df, x_axis, y_axis):
    work = df.copy()

    if y_axis not in work.columns or not pd.api.types.is_numeric_dtype(work[y_axis]):
        return []

    if _is_date_column(work, x_axis):
        work[x_axis] = _parse_dates(work, x_axis)
        work = work.dropna(subset=[x_axis])
        work = work.sort_values(x_axis)
        work[x_axis] = work[x_axis].dt.strftime("%Y-%m-%d")
        grouped = work.groupby(x_axis, sort=True)[y_axis].mean().reset_index()
        grouped[y_axis] = grouped[y_axis].round(2)
        return grouped.to_dict(orient="records")

    if work[x_axis].nunique() <= 30:
        grouped = work.groupby(x_axis, sort=True)[y_axis].mean().reset_index()
        grouped[y_axis] = grouped[y_axis].round(2)
        return grouped.to_dict(orient="records")

    top = work[x_axis].value_counts().head(15).index
    filtered = work[work[x_axis].isin(top)]
    grouped = filtered.groupby(x_axis, sort=True)[y_axis].mean().reset_index()
    grouped[y_axis] = grouped[y_axis].round(2)
    return grouped.to_dict(orient="records")


def _build_bar_data(df, x_axis, y_axis):
    work = df.copy()

    if y_axis not in work.columns or not pd.api.types.is_numeric_dtype(work[y_axis]):
        return []

    n_unique = work[x_axis].nunique()
    if n_unique > 30:
        top = work[x_axis].value_counts().head(15).index
        work = work[work[x_axis].isin(top)]

    grouped = work.groupby(x_axis, sort=True)[y_axis].sum().reset_index()
    grouped[y_axis] = grouped[y_axis].round(2)
    grouped = grouped.sort_values(y_axis, ascending=False)
    return grouped.to_dict(orient="records")


def _build_pie_data(df, x_axis, y_axis):
    work = df.copy()

    if y_axis in work.columns and pd.api.types.is_numeric_dtype(work[y_axis]):
        grouped = work.groupby(x_axis)[y_axis].sum().reset_index()
    else:
        counts = work[x_axis].value_counts().reset_index()
        counts.columns = [x_axis, y_axis]
        grouped = counts

    grouped[y_axis] = grouped[y_axis].round(2)
    grouped = grouped.sort_values(y_axis, ascending=False).head(10)
    return grouped.to_dict(orient="records")
