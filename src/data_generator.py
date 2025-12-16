from __future__ import annotations

import numpy as np
import pandas as pd


def generate_survey_data(n: int = 500, seed: int = 42) -> pd.DataFrame:
    """
    Gera dados sintéticos estilo pesquisa/coleta com erros:
    - missing values
    - inválidos (strings em campo numérico, faixas impossíveis)
    - outliers
    """
    rng = np.random.default_rng(seed)

    df = pd.DataFrame(
        {
            "respondent_id": np.arange(1, n + 1),
            "age": rng.integers(18, 70, size=n),
            "income": rng.normal(4500, 1500, size=n).round(2),  # renda média
            "rating": rng.integers(1, 6, size=n),  # 1..5
            "completion_time_sec": rng.normal(320, 120, size=n).round(0),
        }
    )


    miss_idx = rng.choice(df.index, size=int(n * 0.08), replace=False)
    df.loc[miss_idx, "income"] = np.nan

    miss_idx2 = rng.choice(df.index, size=int(n * 0.04), replace=False)
    df.loc[miss_idx2, "rating"] = np.nan

    inv_idx = rng.choice(df.index, size=int(n * 0.03), replace=False)
    df.loc[inv_idx, "income"] = "invalid"  

    inv_idx2 = rng.choice(df.index, size=int(n * 0.02), replace=False)
    df.loc[inv_idx2, "age"] = -5 

    inv_idx3 = rng.choice(df.index, size=int(n * 0.02), replace=False)
    df.loc[inv_idx3, "rating"] = 9 

    #Outliers
    out_idx = rng.choice(df.index, size=int(n * 0.01), replace=False)
    df.loc[out_idx, "income"] = df["income"].replace("invalid", np.nan).astype(float).max() * 8

    out_idx2 = rng.choice(df.index, size=int(n * 0.01), replace=False)
    df.loc[out_idx2, "completion_time_sec"] = 5  
    df.loc[df["completion_time_sec"] < 10, "completion_time_sec"] = 10

    return df


def save_raw_csv(path: str = "data/raw_data.csv", n: int = 500, seed: int = 42) -> pd.DataFrame:
    df = generate_survey_data(n=n, seed=seed)
    df.to_csv(path, index=False)
    return df


if __name__ == "__main__":
    save_raw_csv()
    print("✅ Gerado: data/raw_data.csv")
