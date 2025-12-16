from __future__ import annotations

import numpy as np
import pandas as pd


def missing_percent(df: pd.DataFrame) -> pd.Series:
    return (df.isna().mean() * 100).round(2)


def invalid_percent(df: pd.DataFrame) -> pd.Series:
    """
    Regras simples de inválidos (você pode expandir):
    - age <= 0 ou age > 110
    - rating fora 1..5
    - income não numérico (string) ou <= 0
    - completion_time_sec <= 0
    """
    invalid = {}

    age = pd.to_numeric(df["age"], errors="coerce")
    invalid["age"] = ((age.isna()) | (age <= 0) | (age > 110)).mean() * 100
    rating = pd.to_numeric(df["rating"], errors="coerce")
    invalid["rating"] = ((rating.isna()) | (rating < 1) | (rating > 5)).mean() * 100
    income = pd.to_numeric(df["income"], errors="coerce")
    invalid["income"] = ((income.isna()) | (income <= 0)).mean() * 100
    t = pd.to_numeric(df["completion_time_sec"], errors="coerce")
    invalid["completion_time_sec"] = ((t.isna()) | (t <= 0)).mean() * 100

    return pd.Series({k: round(v, 2) for k, v in invalid.items()})


def iqr_outliers_mask(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return pd.Series([False] * len(series), index=series.index)
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    full = pd.to_numeric(series, errors="coerce")
    return (full < lower) | (full > upper)


def outliers_percent(df: pd.DataFrame, numeric_cols: list[str]) -> pd.Series:
    res = {}
    for col in numeric_cols:
        mask = iqr_outliers_mask(df[col])
        res[col] = round(mask.mean() * 100, 2)
    return pd.Series(res)
