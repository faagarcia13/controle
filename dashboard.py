import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial da página
st.set_page_config(page_title="Controle de Faturamento", layout="wide")

st.title("📊 Painel de Controle de Faturamentos e Implantações")

# Simulando a sua base de dados (futuramente pode ser um pd.read_excel('planilha.xlsx'))
dados = {
    "Cliente": ["Eduardo", "Rita", "Gabriel", "Felipe", "Gilberto"],
    "Operadora": ["Amil", "Amil", "SulAmérica", "Bradesco", "Amil"],
    "Status": ["Faturado", "Aguardando Documentação", "Revisão de Contrato", "Em Implantação", "Aguardando Assinatura"],
    "Vidas": [7, 4, 15, 5, 12],
    "Valor (R$)": [5000.00, 3200.00, 8500.00, 4100.00, 7600.00]
}
df = pd.DataFrame(dados)

# ---------------------------------------------------
# SEÇÃO 1: CARDS DE RESUMO (Métricas)
# ---------------------------------------------------
total_faturado = df[df["Status"] == "Faturado"]["Valor (R$)"].sum()
em_andamento = df[df["Status"] != "Faturado"]["Valor (R$)"].sum()
total_vidas = df["Vidas"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("✅ Total Faturado", f"R$ {total_faturado:,.2f}")
col2.metric("⏳ Negócios em Andamento", f"R$ {em_andamento:,.2f}")
col3.metric("👥 Vidas Administradas", total_vidas)

st.markdown("---")

# ---------------------------------------------------
# SEÇÃO 2: DASHBOARDS E VISUALIZAÇÃO
# ---------------------------------------------------
col_grafico, col_tabela = st.columns(2)

with col_grafico:
    st.subheader("Distribuição por Status")
    # Gráfico de rosca para ver onde está o volume financeiro
    fig = px.pie(df, names="Status", values="Valor (R$)", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col_tabela:
    st.subheader("Últimas Movimentações")
    # Tabela interativa onde você pode ordenar as colunas
    st.dataframe(df, use_container_width=True, hide_index=True)