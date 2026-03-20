import streamlit as st
from streamlit_card import card
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Refeições IF", layout="wide")

st.title("🍎 Refeições IF")

data = {
    "data": [
        "18/03/2026","18/03/2026","18/03/2026",
        "19/03/2026","19/03/2026","19/03/2026",
        "20/03/2026","20/03/2026","20/03/2026"
    ],

    "refeicao": [
        "Lanche","Almoço","Jantar",
        "Lanche","Almoço","Jantar",
        "Lanche","Almoço","Jantar"
    ],

    "principal": [
        "Pão com queijo",
        "Arroz, feijão e frango grelhado",
        "Sopa",

        "Cuscuz com ovo",
        "feijão e frango grelhado",
        "Arroz, feijão e carne moída",

        "Pão com queijo",
        "Arroz, feijão e frango grelhado",
        "Sopa"
    ],

    "complemento": [
        "Banana",
        None,
        None,

        "Suco de acerola",
        None,
        None,

        "Melancia",
        None,
        None
    ],

    "tipo_complemento": [
        "fruta",
        None,
        None,

        "bebida",
        None,
        None,

        "fruta",
        None,
        None
    ]
}

df = pd.DataFrame(data)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_refeicoes = card(
        title="🍽️ Total de Refeições",
        text=str(len(df))
    )

with col2:
    complemento_mais_servido = df["complemento"].value_counts().idxmax()
    complemento = card(
        title="🥤 Complemento mais servido",
        text=str(complemento_mais_servido)
    )

with col3:
    lanche_mais_servido = df["principal"].value_counts().idxmax()
    complemento = card(
        title="🥪 Lanche mais servido",
        text=str(lanche_mais_servido)
    )

almoco = df[df["refeicao"] == "Almoço"]
with col4:
    almoco_mais_servido = almoco["principal"].value_counts().idxmax()
    card(
        title="🍛 Almoço mais servido",
        text=str(almoco_mais_servido)
    )

col1, col2 = st.columns(2)

with col1:
    lanche = df[df["refeicao"] == "Lanche"]
    lanches = lanche["principal"].value_counts()
    st.subheader("🥪 Lanches mais servidos")
    st.bar_chart(lanches)

with col2:
    complementos = df["complemento"].value_counts().reset_index()
    complementos.columns = ["complemento", "quantidade"]
    fig = px.pie(
        complementos,
        names="complemento",
        values="quantidade",
        title="Complementos mais servidos"
    )

    st.plotly_chart(fig)

almoco = df[df["refeicao"] == "Almoço"]
almocos = almoco["principal"].value_counts()
st.subheader("🍛 Almoços mais servidos")
st.bar_chart(almocos)

st.subheader("Tabela de valores")
st.dataframe(df)