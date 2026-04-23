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

st.sidebar.header("Filtros")

# =========================
# 📊 FILTRO
# =========================

refeicao_filtro = st.sidebar.multiselect(
    "Filtrar por refeição",
    options=df["refeicao"].unique(),
    default=df["refeicao"].unique()
)

df = df[df["refeicao"].isin(refeicao_filtro)]


total_registros = len(df)
item_mais_servido = df["item"].value_counts().idxmax()
refeicao_mais_comum = df["refeicao"].value_counts().idxmax()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🍽️ Total de Registros",
        value=total_registros
    )

with col2:
    st.metric(
        label="🥇 Item mais servido",
        value=item_mais_servido
    )

with col3:
    st.metric(
        label="🍛 Refeição mais comum",
        value=refeicao_mais_comum
    )

col_graficos, col_resumo = st.columns([3,1])

# =========================
# 📊 GRÁFICOS
# =========================
with col_graficos:

    st.subheader("📊 Itens mais servidos")

    itens = df["item"].value_counts()

    fig_itens = px.bar(
        x=itens.index,
        y=itens.values,
        labels={
            "x": "Item",
            "y": "Quantidade"
        },
        title="Itens mais servidos"
    )

    st.plotly_chart(fig_itens, use_container_width=True)

    st.subheader("📊 Tipos de itens")

    tipos = df["tipo_item"].value_counts()

    fig_tipos = px.pie(
        values=tipos.values,
        names=tipos.index,
        title="Distribuição dos tipos de itens"
    )

    st.plotly_chart(fig_tipos, use_container_width=True)

with col_resumo:

    st.subheader("📊 Resumo")

    st.info(f"Total de registros: {total_registros}")

    st.success(f"Item mais servido: {item_mais_servido}")

    st.warning(f"Refeição mais comum: {refeicao_mais_comum}")

# =========================
# 📋 TABELA
# =========================
st.subheader("📋 Dados completos")
st.dataframe(df, use_container_width=True, height=400)