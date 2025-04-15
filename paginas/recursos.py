import streamlit as st
from paginas.funcoes import registrar_atividade_academica

# Título da página
st.title("📚 Recursos")

# Descrição
st.write("Aqui você encontra recursos úteis para consulta:")

# Link para a Tabela TACO
if st.link_button("🥗 Tabela de Nutrientes TACO", "https://docs.google.com/spreadsheets/d/1jqQZ4MkEJ9BCfrMQrpQj-EZt-E3YY5dX3iTCHYyeJ6U/edit?usp=sharing"):
    registrar_atividade_academica(
        tipo="recursos",
        modulo="Recursos",
        detalhes={
            "acao": "acesso_recurso",
            "recurso": "Tabela TACO",
            "tipo_recurso": "planilha"
        }
    ) 