# Data Quality Dashboard (Pesquisa/Coleta)

Dashboard para monitorar qualidade de dados em pipelines de pesquisa/coleta.
O projeto simula dados “sujos” (missing, inválidos e outliers), executa uma etapa de limpeza e exibe a melhoria com métricas e gráficos.

## ✅ O que o dashboard mostra
- % de valores faltantes (missing)
- % de valores inválidos (regras simples)
- % de outliers (IQR)
- Distribuição antes/depois da limpeza
- Alertas (ex.: missing acima de 10%)

## 🧪 Dados
Dados sintéticos gerados por script (sem dados reais).

## 🛠 Stack
- Python (Pandas, NumPy)
- Streamlit
- Matplotlib

## ▶️ Como rodar
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
