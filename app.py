import streamlit as st
import pandas as pd
import plotly.express as px
from joblib import load

st.title("👮‍♂️ Painel de Perícia Odontológica")

@st.cache_data
def load_data():
    return pd.read_csv("data/crimes.csv")

df = load_data()

anos = st.sidebar.multiselect("Ano do crime", options=sorted(df["ano"].unique()))
tipo = st.sidebar.selectbox("Tipo de crime", ["Todos"] + df["tipo"].unique().tolist())

filtro = df.copy()
if anos:
    filtro = filtro[filtro["ano"].isin(anos)]
if tipo != "Todos":
    filtro = filtro[filtro["tipo"] == tipo]

st.write(f"Casos filtrados: {len(filtro)}")

fig_anel = px.pie(filtro, names="tipo", hole=0.5, title="Frequência relativa dos tipos de crime")
st.plotly_chart(fig_anel, use_container_width=True)

fig_box = px.box(filtro, x="tipo", y="qtd_ferimentos", title="Distribuição de ferimentos por tipo de crime")
st.plotly_chart(fig_box, use_container_width=True)

fig_hist = px.histogram(filtro, x="idade_vitima", nbins=20, title="Distribuição das idades das vítimas")
st.plotly_chart(fig_hist, use_container_width=True)

fig_linha = px.line(filtro.groupby("ano").size().reset_index(name="casos"),
                     x="ano", y="casos", markers=True, title="Distribuição dos casos ao longo do tempo")
st.plotly_chart(fig_linha, use_container_width=True)

if "latitude" in filtro.columns and "longitude" in filtro.columns:
    fig_mapa = px.scatter_mapbox(filtro, lat="latitude", lon="longitude", color="tipo", 
                                 title="Distribuição espacial dos casos",
                                 mapbox_style="open-street-map", zoom=3)
    st.plotly_chart(fig_mapa, use_container_width=True)

modelo = load("modelo.joblib")

st.header("🔍 Previsão rápida")
col1, col2, col3 = st.columns(3)
idade = col1.number_input("Idade vítima", 0, 120, 35)
ano_x = col2.number_input("Ano", 2005, 2025, 2020)
ferimentos = col3.number_input("Nº ferimentos", 0, 50, 1)

if st.button("Prever se o caso será resolvido"):
    pred = modelo.predict([[idade, ano_x, ferimentos]])[0]
    st.success("Provavelmente SERÁ resolvido! 🎉" if pred == 1 else "Hmm, chance de NÃO ser resolvido.")