import os
import sys

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from src.data_generator import save_raw_csv
from src.data_cleaning import save_clean_csv
from src.data_quality import missing_percent, invalid_percent, outliers_percent


st.set_page_config(page_title="Data Quality Dashboard", layout="wide")
st.title("📊 Data Quality Dashboard — Pesquisa/Coleta")

st.sidebar.header("Controles")
n = st.sidebar.slider("Qtd. de linhas (dados sintéticos)", min_value=200, max_value=5000, value=800, step=100)
seed = st.sidebar.number_input("Seed", min_value=0, max_value=999999, value=42, step=1)
missing_alert_threshold = st.sidebar.slider("Alerta de missing (%)", 1, 50, 10)

if st.sidebar.button("🔄 Gerar dados + limpar"):
    save_raw_csv(path="data/raw_data.csv", n=n, seed=seed)
    save_clean_csv(raw_path="data/raw_data.csv", clean_path="data/clean_data.csv")
    st.sidebar.success("Dados gerados e limpos ✅")
if not os.path.exists("data/raw_data.csv"):
    save_raw_csv(path="data/raw_data.csv", n=n, seed=seed)
if not os.path.exists("data/clean_data.csv"):
    save_clean_csv(raw_path="data/raw_data.csv", clean_path="data/clean_data.csv")

raw = pd.read_csv("data/raw_data.csv")
clean = pd.read_csv("data/clean_data.csv")

col1, col2, col3 = st.columns(3)

raw_missing = missing_percent(raw)
raw_invalid = invalid_percent(raw)
raw_outliers = outliers_percent(raw, numeric_cols=["age", "income", "rating", "completion_time_sec"])

with col1:
    st.subheader("📌 Missing (%) — bruto")
    st.dataframe(raw_missing.rename("missing_%"))

with col2:
    st.subheader("🚫 Inválidos (%) — bruto")
    st.dataframe(raw_invalid.rename("invalid_%"))

with col3:
    st.subheader("📈 Outliers IQR (%) — bruto")
    st.dataframe(raw_outliers.rename("outliers_%"))

st.subheader("🚨 Alertas")
max_missing = float(raw_missing.max())
if max_missing >= missing_alert_threshold:
    st.warning(f"Missing alto: {max_missing:.2f}% (limite: {missing_alert_threshold}%). Verifique colunas com mais missing.")
else:
    st.success(f"Missing OK: máximo {max_missing:.2f}% (limite: {missing_alert_threshold}%).")

st.subheader("🔎 Distribuição antes/depois da limpeza")

metric_col = st.selectbox("Escolha uma variável numérica:", ["age", "income", "rating", "completion_time_sec"])

c1, c2 = st.columns(2)

with c1:
    st.caption("Antes (raw)")
    fig = plt.figure()
    plt.hist(pd.to_numeric(raw[metric_col], errors="coerce").dropna(), bins=30)
    st.pyplot(fig, clear_figure=True)

with c2:
    st.caption("Depois (clean)")
    fig = plt.figure()
    plt.hist(pd.to_numeric(clean[metric_col], errors="coerce").dropna(), bins=30)
    st.pyplot(fig, clear_figure=True)

st.subheader("🧾 Amostras de dados")
t1, t2 = st.columns(2)

with t1:
    st.caption("Raw (primeiras 20 linhas)")
    st.dataframe(raw.head(20))

with t2:
    st.caption("Clean (primeiras 20 linhas)")
    st.dataframe(clean.head(20))
