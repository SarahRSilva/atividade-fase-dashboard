import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AgroSmart — Inspeção de Batatas", page_icon="🥔", layout="wide")

st.title("🥔 AgroSmart — Dashboard de Inspeção de Batatas")
st.caption("Fase 2 | Visão computacional aplicada ao controle de qualidade de batatas")

# --- Upload ou arquivo padrão (atende requisito 1.2) ---
uploaded = st.sidebar.file_uploader("📤 Atualizar com novo CSV da Fase 1", type="csv")
if uploaded:
    df = pd.read_csv(uploaded, sep=";")
    st.sidebar.success(f"{len(df)} novos registros carregados")
else:
    df = pd.read_csv("dados/inspecoes.csv", sep=";")

df["Data_Inspecao"] = pd.to_datetime(df["Data_Inspecao"])

# --- Filtros ---
st.sidebar.header("🔎 Filtros")
locs = st.sidebar.multiselect("Localidade", df["Localidade"].unique(), default=df["Localidade"].unique())
talhoes = st.sidebar.multiselect("Talhão", df["Talhao"].unique(), default=df["Talhao"].unique())
confianca_min = st.sidebar.slider("Confiança mínima (%)", 0, 100, 0)

dff = df[
    df["Localidade"].isin(locs) &
    df["Talhao"].isin(talhoes) &
    (df["Grau_de_Confianca_Pct"] >= confianca_min)
]

# --- KPIs ---
total = len(dff)
doentes = (dff["Status_Inspecao"] == "Doente").sum()
saudaveis = total - doentes
conf_media = dff["Grau_de_Confianca_Pct"].mean() if total else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("🖼️ Imagens analisadas", total)
c2.metric("✅ Saudáveis", f"{saudaveis} ({saudaveis/total*100:.1f}%)" if total else "0")
c3.metric("⚠️ Doentes", f"{doentes} ({doentes/total*100:.1f}%)" if total else "0",
          delta=f"-{doentes/total*100:.1f}% da produção" if total else None, delta_color="inverse")
c4.metric("🎯 Confiança média do modelo", f"{conf_media:.1f}%")

# --- Gráficos ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribuição geral")
    fig = px.pie(dff, names="Status_Inspecao", color="Status_Inspecao",
                 color_discrete_map={"Saudavel": "#2ecc71", "Doente": "#e74c3c"}, hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Tipos de doença detectados")
    doen = dff[dff["Status_Inspecao"] == "Doente"].groupby("Tipo_Doenca").size().reset_index(name="Qtd")
    fig = px.bar(doen, x="Tipo_Doenca", y="Qtd", color="Qtd", color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Tendência temporal (últimos 90 dias)")
serie = dff.groupby([dff["Data_Inspecao"].dt.date, "Status_Inspecao"]).size().reset_index(name="Qtd")
serie.columns = ["Data", "Status", "Qtd"]
fig = px.line(serie, x="Data", y="Qtd", color="Status", markers=True,
              color_discrete_map={"Saudavel": "#2ecc71", "Doente": "#e74c3c"})
st.plotly_chart(fig, use_container_width=True)

st.subheader("🗺️ Taxa de doença por localidade e talhão")
heat = dff.groupby(["Localidade", "Talhao"]).apply(
    lambda x: (x["Status_Inspecao"] == "Doente").mean() * 100
).reset_index(name="Pct_Doentes")
fig = px.density_heatmap(heat, x="Talhao", y="Localidade", z="Pct_Doentes",
                          color_continuous_scale="Reds", text_auto=".1f")
st.plotly_chart(fig, use_container_width=True)

# --- Insights automáticos (bom pro vídeo!) ---
st.subheader("💡 Alertas e recomendações")
talhao_critico = heat.loc[heat["Pct_Doentes"].idxmax()] if len(heat) else None
if talhao_critico is not None and talhao_critico["Pct_Doentes"] > 30:
    st.error(f"🚨 **Ação urgente**: {talhao_critico['Localidade']} / Talhão {talhao_critico['Talhao']} "
             f"apresenta {talhao_critico['Pct_Doentes']:.1f}% de batatas doentes. "
             f"Recomenda-se inspeção presencial e aplicação preventiva de fungicida nos talhões vizinhos.")

doenca_freq = dff[dff["Status_Inspecao"] == "Doente"]["Tipo_Doenca"].mode()
if len(doenca_freq):
    st.warning(f"⚠️ Doença mais recorrente: **{doenca_freq[0]}** — priorizar manejo específico.")

st.dataframe(dff, use_container_width=True)