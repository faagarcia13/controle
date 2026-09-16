import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Controle de Faturamento", layout="wide")

# Nome do nosso arquivo que servirá de banco de dados
ARQUIVO_DADOS = "faturamentos.csv"

# Função para carregar os dados salvos
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        return pd.read_csv(ARQUIVO_DADOS)
    else:
        # Se o arquivo não existir ainda, criamos a estrutura das colunas
        return pd.DataFrame(columns=["Empresa", "CNPJ", "Vidas", "Valor Boleto (R$)", "Mês Referência", "Status"])

df = carregar_dados()

# Criando duas abas no topo do sistema
aba_dashboard, aba_cadastro = st.tabs(["📊 Dashboard", "📝 Cadastrar Empresa"])

# ---------------------------------------------------
# ABA DE CADASTRO
# ---------------------------------------------------
with aba_cadastro:
    st.header("Cadastrar Nova Movimentação")
    
    # O st.form garante que a tela só atualize quando você clicar em Salvar
    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)
        
        with col1:
            empresa = st.text_input("Nome da Empresa / Cliente")
            cnpj = st.text_input("CNPJ (Apenas números)")
            vidas = st.number_input("Número de Vidas", min_value=1, step=1)
            
        with col2:
            valor = st.number_input("Valor Mensal do Boleto (R$)", min_value=0.0, step=100.0, format="%.2f")
            mes = st.selectbox("Mês de Referência", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
            status = st.selectbox("Faturamento já foi gerado?", ["Não (Pendente)", "Sim (Faturado)"])
            
        botao_salvar = st.form_submit_button("Salvar Cadastro")
        
        if botao_salvar:
            if empresa == "":
                st.error("O nome da empresa é obrigatório!")
            else:
                # Criando a nova linha com os dados preenchidos
                novo_dado = pd.DataFrame([{
                    "Empresa": empresa,
                    "CNPJ": cnpj,
                    "Vidas": vidas,
                    "Valor Boleto (R$)": valor,
                    "Mês Referência": mes,
                    "Status": status
                }])
                
                # Juntando com os dados antigos e salvando no CSV
                df = pd.concat([df, novo_dado], ignore_index=True)
                df.to_csv(ARQUIVO_DADOS, index=False)
                
                st.success(f"Movimentação da empresa {empresa} cadastrada com sucesso!")
                # O comando abaixo recarrega a página para o Dashboard atualizar na hora
                st.rerun()

# ---------------------------------------------------
# ABA DE DASHBOARD
# ---------------------------------------------------
with aba_dashboard:
    st.title("📊 Painel de Faturamentos")
    
    if df.empty:
        st.info("Nenhum dado cadastrado ainda. Vá na aba 'Cadastrar Empresa' para começar.")
    else:
        # Convertendo valores para garantir que o Python entenda como números
        df["Valor Boleto (R\()"] = pd.to_numeric(df["Valor Boleto (R\))"])
        df["Vidas"] = pd.to_numeric(df["Vidas"])

        # Separando o que foi faturado do que está pendente
        total_faturado = df[df["Status"] == "Sim (Faturado)"]["Valor Boleto (R$)"].sum()
        pendente = df[df["Status"] == "Não (Pendente)"]["Valor Boleto (R$)"].sum()
        total_vidas = df["Vidas"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("✅ Total Faturado", f"R$ {total_faturado:,.2f}")
        c2.metric("⏳ Faturamento Pendente", f"R$ {pendente:,.2f}")
        c3.metric("👥 Vidas Administradas", int(total_vidas))
        
        st.markdown("---")
        
        col_graf, col_tab = st.columns(2)
        
        with col_graf:
            st.subheader("Status dos Recebimentos")
            # Gráfico com cores personalizadas (Verde para Faturado, Vermelho para Pendente)
            fig = px.pie(df, names="Status", values="Valor Boleto (R$)", hole=0.4, 
                         color="Status", color_discrete_map={"Sim (Faturado)": "#28a745", "Não (Pendente)": "#dc3545"})
            st.plotly_chart(fig, use_container_width=True)
            
        with col_tab:
            st.subheader("Últimos Cadastros")
            st.dataframe(df, use_container_width=True, hide_index=True)
