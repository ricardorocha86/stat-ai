import streamlit as st
from paginas.funcoes import registrar_atividade_academica
import os
import pandas as pd

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

# Seção de Gabarito Interativo da Lista 5
st.subheader("📝 Gabarito Interativo - Lista 5")
st.info("Selecione um exercício abaixo. A resolução será mostrada passo a passo, para que você possa tentar resolver antes de ver a resposta.")

try:
    caminho_gabarito = "code.txt"
    df_gabarito = pd.read_csv(caminho_gabarito)

    # Inicializa o estado da sessão para controlar a visibilidade dos passos
    if 'gabarito_step' not in st.session_state:
        st.session_state.gabarito_step = 0  # 0: Nada selecionado, 1: Dica 1, 2: Dica 2, 3: Resolução, 4: Final
    if 'gabarito_q' not in st.session_state:
        st.session_state.gabarito_q = None
    if 'gabarito_item' not in st.session_state:
        st.session_state.gabarito_item = None

    # Função para reiniciar o processo ao selecionar nova questão/item
    def reiniciar_passos():
        st.session_state.gabarito_step = 1

    questoes_disponiveis = df_gabarito['Questão'].unique()
    
    # --- Seleção da Questão ---
    selected_q = st.selectbox(
        "**1. Selecione a Questão:**",
        options=questoes_disponiveis,
        index=None,
        placeholder="Escolha um exercício...",
        on_change=reiniciar_passos
    )

    if selected_q:
        if st.session_state.gabarito_step == 0:
            reiniciar_passos()

        df_da_questao = df_gabarito[df_gabarito['Questão'] == selected_q]
        itens_da_questao = df_da_questao['Item'].unique()
        
        selected_item = None
        # --- Seleção do Item (se houver) ---
        if len(itens_da_questao) > 1 or (len(itens_da_questao) == 1 and itens_da_questao[0] != "Único"):
            selected_item = st.selectbox(
                "**2. Selecione o Item:**",
                options=itens_da_questao,
                on_change=reiniciar_passos,
                key=f"item_select_{selected_q}"
            )
        else:
            selected_item = itens_da_questao[0]

        if selected_item:
            # Puxa os dados do exercício e item selecionados
            dados = df_da_questao[df_da_questao['Item'] == selected_item].iloc[0]

            # --- Lógica de Exibição Passo a Passo ---
            st.markdown("---")

            # Passo 1: Dica Geral
            if st.session_state.gabarito_step >= 1:
                with st.container(border=True):
                    st.markdown("##### 💡 Dica Geral")
                    st.markdown(dados['Dica Geral'])
                if st.session_state.gabarito_step == 1:
                    if st.button("Ver Dica Mais Específica", use_container_width=True):
                        st.session_state.gabarito_step = 2
                        st.rerun()

            # Passo 2: Dica Menos Geral
            if st.session_state.gabarito_step >= 2:
                with st.container(border=True):
                    st.markdown("##### 🔍 Dica Mais Específica")
                    st.markdown(dados['Dica Menos Geral'])
                if st.session_state.gabarito_step == 2:
                    if st.button("Ver Resolução Comentada", use_container_width=True):
                        st.session_state.gabarito_step = 3
                        st.rerun()

            # Passo 3: Resolução
            if st.session_state.gabarito_step >= 3:
                with st.container(border=True):
                    st.markdown("##### 👨‍🏫 Resolução Comentada")
                    st.markdown(dados['Resolução'], unsafe_allow_html=True)
                if st.session_state.gabarito_step == 3:
                    if st.button("Ver Gabarito Final", use_container_width=True):
                        st.session_state.gabarito_step = 4
                        st.rerun()

            # Passo 4: Gabarito Final
            if st.session_state.gabarito_step >= 4:
                with st.container(border=True):
                    st.markdown("##### ✅ Gabarito Final")
                    st.markdown(dados['Gabarito Final'])
                if st.button("Ocultar Resolução", use_container_width=True):
                    reiniciar_passos()
                    st.rerun()

except FileNotFoundError:
    st.error(f"Arquivo de gabarito ('{caminho_gabarito}') não encontrado. Verifique se o arquivo está na pasta principal do projeto.")
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o gabarito interativo: {e}")

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