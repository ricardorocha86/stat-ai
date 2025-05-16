import streamlit as st
import json
import os
# Removido: from openai import OpenAI 
# Adicionado: Importa a função de IA modularizada
from paginas.llms import avaliar_resposta_exercicio
from paginas.funcoes import registrar_atividade_academica, registrar_acao_usuario

st.title("🤖 Corretor AI")

# --- Seleção da Lista de Exercícios ---
mapa_listas = {
    "Lista 1": "arquivos/lista1.json",
    "Lista 2": "arquivos/lista2.json"
}
lista_selecionada_nome = st.selectbox(
    "Escolha a lista de exercícios:", 
    options=list(mapa_listas.keys()), 
    key="select_lista_corretor"
)

caminho_json_exercicios = mapa_listas[lista_selecionada_nome]

# --- Carregar Dados dos Exercícios ---
@st.cache_data # Adicionar cache para otimizar o carregamento do JSON
def carregar_exercicios(caminho_json):
    try:
        with open(caminho_json, "r", encoding="utf-8") as file:
            data = json.load(file)
        # Verifica se a estrutura básica existe
        if "exercicios" in data and isinstance(data["exercicios"], list):
            return data["exercicios"]
        else:
            st.error(f"Erro: O arquivo JSON '{caminho_json}' não contém a chave 'exercicios' ou não é uma lista.")
            return []
    except FileNotFoundError:
        st.error(f"Erro: Arquivo de exercícios '{caminho_json}' não encontrado.")
        return []
    except json.JSONDecodeError:
        st.error(f"Erro: O arquivo '{caminho_json}' não é um JSON válido.")
        return []
    except Exception as e:
        st.error(f"Erro inesperado ao carregar exercícios: {e}")
        return []

exercicios_data = carregar_exercicios(caminho_json_exercicios)

# --- Conteúdo da Página (Seleção e Exibição) ---
if not exercicios_data:
    st.warning(f"Nenhum exercício carregado para a {lista_selecionada_nome}. Verifique o arquivo JSON correspondente.")
else:
    st.markdown(f"Selecione um exercício da **{lista_selecionada_nome}** abaixo para visualizar seu enunciado e usar a ferramenta de avaliação de resposta.")
    
    opcoes = [f"{ex.get('numero', 'N/A')}. {ex.get('titulo', 'Sem Título')}" for ex in exercicios_data]
    # Chave do selectbox de exercício agora é dinâmica com base na lista selecionada
    selecionado_label = st.selectbox(
        "Selecione o exercício:", 
        opcoes, 
        key=f"select_ex_{lista_selecionada_nome.replace(' ', '_')}"
    )

    if selecionado_label:
        registrar_atividade_academica(
            tipo="exercicio_corretor_ai", # Modificado para refletir a página
            modulo=lista_selecionada_nome,
            detalhes={
                "acao": "visualizacao_exercicio",
                "exercicio": selecionado_label
            }
        )

    st.divider()

    exercicio_selecionado = next((item for item in exercicios_data if f"{item.get('numero', 'N/A')}. {item.get('titulo', 'Sem Título')}" == selecionado_label), None)

    if exercicio_selecionado:
        st.subheader(f"Exercício {exercicio_selecionado.get('numero', '')}: {exercicio_selecionado.get('titulo', '')}")
        
        # Verifica se há conteúdo antes de exibir
        conteudo_exercicio = exercicio_selecionado.get("conteudo", "")
        if conteudo_exercicio:
             st.markdown(conteudo_exercicio)
        else:
             st.info("Este exercício não possui um enunciado detalhado no arquivo JSON.")

        st.divider()
        
        # --- Ferramenta: Avaliar Resposta AI --- 
        st.subheader("⚖️ Avalie Sua Resposta com IA")
        st.info("Cole sua resposta para o exercício acima e peça uma avaliação direta.")

        enunciado_para_avaliacao = conteudo_exercicio if conteudo_exercicio else selecionado_label
        # Chaves da área de texto e botão agora são dinâmicas
        key_sufixo = lista_selecionada_nome.replace(' ', '_')
        resposta_aluno = st.text_area("✏️ Sua Resposta:", height=150, key=f"resposta_ex_{key_sufixo}")

        if st.button("⚖️ Avaliar minha resposta", key=f"btn_avaliar_ex_{key_sufixo}", type="primary"):
            if not resposta_aluno:
                st.warning("Por favor, insira a sua resposta.")
            else:
                with st.spinner("Avaliando sua resposta..."):
                    response_content = avaliar_resposta_exercicio(enunciado_para_avaliacao, resposta_aluno)
                    if response_content:
                        with st.chat_message("assistant", avatar='⚖️'):
                            # Aplicar substituições para renderização matemática do Streamlit
                            response_content_render = response_content.replace("\\(", "$").replace("\\)", "$")
                            response_content_render = response_content_render.replace("\[", "$$").replace("\]", "$$")
                            st.markdown(response_content_render)
                            registrar_atividade_academica(
                                tipo="exercicio_corretor_ai", # Modificado
                                modulo=lista_selecionada_nome,
                                detalhes={
                                    "acao": "avaliacao_resposta_ia",
                                    "exercicio": selecionado_label,
                                    "tamanho_resposta": len(resposta_aluno)
                                }
                            )
                    # Erros já são tratados dentro da função avaliar_resposta_exercicio
    else:
        st.info(f"Selecione um exercício na lista ({lista_selecionada_nome}) acima para ver os detalhes.") 