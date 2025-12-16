from __future__ import annotations

import pandas as pd
import numpy as np

from .data_quality import iqr_outliers_mask


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    cleaned["age"] = pd.to_numeric(cleaned["age"], errors="coerce")
    cleaned["income"] = pd.to_numeric(cleaned["income"], errors="coerce")
    cleaned["rating"] = pd.to_numeric(cleaned["rating"], errors="coerce")
    cleaned["completion_time_sec"] = pd.to_numeric(cleaned["completion_time_sec"], errors="coerce")
    cleaned.loc[(cleaned["age"] <= 0) | (cleaned["age"] > 110), "age"] = np.nan
    cleaned.loc[(cleaned["rating"] < 1) | (cleaned["rating"] > 5), "rating"] = np.nan
    cleaned.loc[(cleaned["income"] <= 0), "income"] = np.nan
    cleaned.loc[(cleaned["completion_time_sec"] <= 0), "completion_time_sec"] = np.nan

    for col in ["income", "completion_time_sec"]:
        mask = iqr_outliers_mask(cleaned[col])
        cleaned.loc[mask, col] = np.nan

    cleaned["age"] = cleaned["age"].fillna(cleaned["age"].median())
    cleaned["income"] = cleaned["income"].fillna(cleaned["income"].median())
    if cleaned["rating"].dropna().empty:
        cleaned["rating"] = cleaned["rating"].fillna(3)
    else:
        cleaned["rating"] = cleaned["rating"].fillna(cleaned["rating"].mode().iloc[0])
    cleaned["completion_time_sec"] = cleaned["completion_time_sec"].fillna(cleaned["completion_time_sec"].median())

    cleaned["age"] = cleaned["age"].round(0).astype(int)
    cleaned["rating"] = cleaned["rating"].round(0).astype(int)
    cleaned["completion_time_sec"] = cleaned["completion_time_sec"].round(0).astype(int)

    return cleaned


def save_clean_csv(raw_path: str = "data/raw_data.csv", clean_path: str = "data/clean_data.csv") -> pd.DataFrame:
    raw = pd.read_csv(raw_path)
    cleaned = clean_data(raw)
    cleaned.to_csv(clean_path, index=False)
    return cleaned


if __name__ == "__main__":
    save_clean_csv()
    print("✅ Gerado: data/clean_data.csv")
