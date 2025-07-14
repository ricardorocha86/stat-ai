import streamlit as st
from paginas.funcoes import registrar_atividade_academica
import os

# Título da página
st.title("📚 Listas de Exercícios")
 

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
                use_container_width=False,
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

# Download do PDF da Lista 4
caminho_pdf_exercicios_4 = "arquivos/lista4_exercicios.pdf"
if os.path.exists(caminho_pdf_exercicios_4):
    try:
        with open(caminho_pdf_exercicios_4, "rb") as pdf_file_4:
            st.download_button(
                label="📥 Baixar Lista 4 de Estatística (PDF)",
                data=pdf_file_4,
                file_name="lista4_exercicios_estatistica.pdf",
                mime="application/pdf",
                use_container_width=False,
                on_click=lambda: registrar_atividade_academica(
                    tipo="recurso_download",
                    modulo="Lista 4 PDF",
                    detalhes={
                        "acao": "download_pdf_exercicios",
                        "arquivo": "lista4_exercicios_estatistica.pdf"
                    }
                )
            )
    except Exception as e:
        st.error(f"Erro ao ler PDF da Lista 4: {e}")
else:
    st.warning(f"Arquivo da Lista 4 de Exercícios (PDF) não encontrado em '{caminho_pdf_exercicios_4}'.")

# Download do PDF da Lista 5
caminho_pdf_exercicios_5 = "arquivos/lista5_exercicios.pdf"
if os.path.exists(caminho_pdf_exercicios_5):
    try:
        with open(caminho_pdf_exercicios_5, "rb") as pdf_file_5:
            st.download_button(
                label="📥 Baixar Lista 5 de Estatística (PDF)",
                data=pdf_file_5,
                file_name="lista5_exercicios_estatistica.pdf",
                mime="application/pdf",
                use_container_width=False,
                on_click=lambda: registrar_atividade_academica(
                    tipo="recurso_download",
                    modulo="Lista 5 PDF",
                    detalhes={
                        "acao": "download_pdf_exercicios",
                        "arquivo": "lista5_exercicios_estatistica.pdf"
                    }
                )
            )
    except Exception as e:
        st.error(f"Erro ao ler PDF da Lista 5: {e}")
else:
    st.warning(f"Arquivo da Lista 5 de Exercícios (PDF) não encontrado em '{caminho_pdf_exercicios_5}'.")

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

st.divider()

# Seção de Distribuições de Probabilidade
st.subheader("📊 Distribuições de Probabilidade")
st.write("Visualize diferentes distribuições de probabilidade e suas características:")
st.markdown('[Acessar o site de Distribuições de Probabilidade](https://sites.google.com/view/distprobs/)')
# Incorpora o arquivo HTML com as distribuições de probabilidade
st.components.v1.iframe("static/probs.html", height=1000)