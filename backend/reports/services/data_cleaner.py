import pandas as pd


def clean_data(df):
    log = {
        "duplicates_removed": 0,
        "columns_dropped": [],
        "nulls_imputed": {},
        "rows_dropped_nulls": 0,
        "date_normalized": [],
        "strings_cleaned": [],
    }

    original_rows = len(df)

    dup_count = int(df.duplicated().sum())
    if dup_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)
    log["duplicates_removed"] = dup_count

    missing_pct = df.isna().mean() * 100
    cols_to_drop = missing_pct[missing_pct > 50].index.tolist()
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
    log["columns_dropped"] = cols_to_drop

    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        null_count = int(df[col].isna().sum())
        if null_count > 0:
            median = df[col].median()
            df[col] = df[col].fillna(median)
            log["nulls_imputed"][col] = {"method": "median", "value": float(median), "count": null_count}

    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%S")
        log["date_normalized"].append(col)

    for col in df.select_dtypes(include=["object"]).columns:
        try:
            parsed_dates = pd.to_datetime(df[col].dropna(), errors="raise")
            if len(parsed_dates) > 0:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%S")
                log["date_normalized"].append(col)
                continue
        except (ValueError, TypeError):
            pass

        non_null = df[col].dropna()
        if len(non_null) > 0 and non_null.str.contains(r"\s").any():
            df[col] = df[col].str.strip()
            df[col] = df[col].str.lower()
            log["strings_cleaned"].append(col)

    rows_before = len(df)
    df = df.dropna().reset_index(drop=True)
    dropped = rows_before - len(df)
    log["rows_dropped_nulls"] = dropped

    return df, log
