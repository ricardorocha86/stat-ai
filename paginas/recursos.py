import streamlit as st
from paginas.funcoes import registrar_atividade_academica
import os

# Título da página
st.title("📚 Recursos")

# Descrição
st.write("Aqui você encontra recursos úteis para consulta:")

st.divider()

# --- Seção: Listas de Exercícios Prontas ---
st.subheader("Listas de Exercícios Prontas")

# Download do PDF (movido de paginas/exercicios.py)
caminho_pdf_exercicios = "arquivos/lista1.pdf"
if os.path.exists(caminho_pdf_exercicios):
    try:
        with open(caminho_pdf_exercicios, "rb") as pdf_file:
            st.download_button(
                label="📥 Baixar Lista 1 de Estatística (PDF)",
                data=pdf_file,
                file_name="lista1_exercicios_estatistica.pdf",
                mime="application/pdf",
                use_container_width=False,
                on_click=lambda: registrar_atividade_academica(
                    tipo="recurso_download", # Tipo alterado para refletir a seção
                    modulo="Lista 1 PDF",
                    detalhes={
                        "acao": "download_pdf_exercicios",
                        "arquivo": "lista1_exercicios_estatistica.pdf"
                    }
                )
            )
    except Exception as e:
        st.error(f"Erro ao ler PDF: {e}")
else:
    st.warning(f"Arquivo da Lista 1 de Exercícios (PDF) não encontrado em '{caminho_pdf_exercicios}'.")

# Download do PDF da Lista 2
caminho_pdf_exercicios_2 = "arquivos/lista2_exercicios.pdf"
if os.path.exists(caminho_pdf_exercicios_2):
    try:
        with open(caminho_pdf_exercicios_2, "rb") as pdf_file_2:
            st.download_button(
                label="📥 Baixar Lista 2 de Estatística (PDF)",
                data=pdf_file_2,
                file_name="lista2_exercicios_estatistica.pdf",
                mime="application/pdf",
                use_container_width=False, # Mantém consistência com o botão da Lista 1
                on_click=lambda: registrar_atividade_academica(
                    tipo="recurso_download",
                    modulo="Lista 2 PDF",
                    detalhes={
                        "acao": "download_pdf_exercicios",
                        "arquivo": "lista2_exercicios_estatistica.pdf"
                    }
                )
            )
    except Exception as e:
        st.error(f"Erro ao ler PDF da Lista 2: {e}")
else:
    st.warning(f"Arquivo da Lista 2 de Exercícios (PDF) não encontrado em '{caminho_pdf_exercicios_2}'.")


# Download do PDF da Lista 3
caminho_pdf_exercicios_3 = "arquivos/lista3_exercicios.pdf"
if os.path.exists(caminho_pdf_exercicios_3):
    try:
        with open(caminho_pdf_exercicios_3, "rb") as pdf_file_3:
            st.download_button(
                label="📥 Baixar Lista 3 de Estatística (PDF)",
                data=pdf_file_3,
                file_name="lista3_exercicios_estatistica.pdf",
                mime="application/pdf",
                use_container_width=False, # Mantém consistência com o botão da Lista 1
                on_click=lambda: registrar_atividade_academica(
                    tipo="recurso_download",
                    modulo="Lista 3 PDF",
                    detalhes={
                        "acao": "download_pdf_exercicios",
                        "arquivo": "lista3_exercicios_estatistica.pdf"
                    }
                )
            )
    except Exception as e:
        st.error(f"Erro ao ler PDF da Lista 3: {e}")
else:
    st.warning(f"Arquivo da Lista 3 de Exercícios (PDF) não encontrado em '{caminho_pdf_exercicios_3}'.")

st.divider()

# Link para a Tabela TACO (mantido do código original)
st.subheader("Outros Recursos Úteis")
if st.link_button("🥗 Tabela de Nutrientes TACO", "https://docs.google.com/spreadsheets/d/1jqQZ4MkEJ9BCfrMQrpQj-EZt-E3YY5dX3iTCHYyeJ6U/edit?usp=sharing"):
    registrar_atividade_academica(
        tipo="recursos",
        modulo="Recursos Externos", # Modificado para melhor categorização
        detalhes={
            "acao": "acesso_recurso",
            "recurso": "Tabela TACO",
            "tipo_recurso": "planilha_externa"
        }
    ) 
