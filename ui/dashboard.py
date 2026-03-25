import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from streamlit_card import card
import plotly.express as px
import pandas as pd
from src.core import get_full_data

st.set_page_config(page_title="Refeições IF", layout="wide")

st.title("🍎 Refeições IF")

data = get_full_data()

df = pd.DataFrame(data, columns=[
    "data", "dia_semana", "refeicao", "item", "tipo_item"
])



#Se banco estiver vazio
if df.empty:
    st.warning("⚠️ Nenhum dado encontrado no banco.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🍽️ Total de Registros", len(df))

with col2:
    item_mais_servido = df["item"].value_counts().idxmax()
    st.metric("🥇 Item mais servido", item_mais_servido)

with col3:
    refeicao_mais_comum = df["refeicao"].value_counts().idxmax()
    st.metric("🍛 Refeição mais comum", refeicao_mais_comum)

# =========================
# 📊 FILTRO
# =========================
st.sidebar.header("Filtros")

refeicao_filtro = st.sidebar.multiselect(
    "Filtrar por refeição",
    options=df["refeicao"].unique(),
    default=df["refeicao"].unique()
)

df = df[df["refeicao"].isin(refeicao_filtro)]

# =========================
# 📊 GRÁFICOS
# =========================
st.subheader("📊 Itens mais servidos")

itens = df["item"].value_counts()
st.bar_chart(itens)

st.subheader("📊 Tipos de itens")

tipos = df["tipo_item"].value_counts()
st.bar_chart(tipos)

# =========================
# 📋 TABELA
# =========================
st.subheader("📋 Dados completos")
st.dataframe(df)