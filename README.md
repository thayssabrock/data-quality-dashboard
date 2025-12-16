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

```
## ♦ Imagens

<img width="1902" height="767" alt="image" src="https://github.com/user-attachments/assets/e332eff9-0aaf-4795-9703-270bf83215fa" />
<img width="1913" height="784" alt="image" src="https://github.com/user-attachments/assets/d0adcd9e-d57b-4f4c-a3fb-43e4f72d792d" />
<img width="1886" height="767" alt="image" src="https://github.com/user-attachments/assets/5acad613-9fc4-4fc1-b7cd-f11de2567c2a" />



