import streamlit as st
import json
import os
# Removido: from openai import OpenAI 
# Adicionado: Importa a função de IA modularizada
from paginas.llms import avaliar_resposta_exercicio
from paginas.funcoes import registrar_atividade_academica, registrar_acao_usuario

st.title("🤖 Corretor AI")

# --- Carregar Dados dos Exercícios ---
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

caminho_json_exercicios = "arquivos/lista1.json"
exercicios_data = carregar_exercicios(caminho_json_exercicios)

# --- Conteúdo da Página (Seleção e Exibição) ---
if not exercicios_data:
    st.warning("Nenhum exercício carregado. Verifique o arquivo JSON.")
else:
    st.markdown("Selecione um exercício da lista abaixo para visualizar seu enunciado e usar a ferramenta de avaliação de resposta.")
    # Cria uma lista de opções com os títulos dos exercícios
    opcoes = [f"{ex.get('numero', 'N/A')}. {ex.get('titulo', 'Sem Título')}" for ex in exercicios_data]
    selecionado_label = st.selectbox("Selecione o exercício:", opcoes, key="select_ex")

    if selecionado_label:  # Registra quando um exercício é selecionado
        registrar_atividade_academica(
            tipo="exercicio",
            modulo="Lista 1",
            detalhes={
                "acao": "visualizacao",
                "exercicio": selecionado_label
            }
        )

    st.divider()

    # Procura pelo exercício selecionado
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
        resposta_aluno = st.text_area("✏️ Sua Resposta:", height=150, key="avaliar_resposta_ex")

        if st.button("⚖️ Avaliar minha resposta", key="btn_avaliar_ex", type="primary"):
            if not resposta_aluno:
                st.warning("Por favor, insira a sua resposta.")
            else:
                with st.spinner("Avaliando sua resposta..."):
                    response_content = avaliar_resposta_exercicio(enunciado_para_avaliacao, resposta_aluno)
                    if response_content:
                        with st.chat_message("assistant", avatar='⚖️'):
                            st.markdown(response_content)
                            # Registra a avaliação da resposta
                            registrar_atividade_academica(
                                tipo="exercicio",
                                modulo="Lista 1",
                                detalhes={
                                    "acao": "avaliacao_resposta",
                                    "exercicio": selecionado_label,
                                    "tamanho_resposta": len(resposta_aluno)
                                }
                            )
                    # Erros já são tratados dentro da função avaliar_resposta_exercicio
    else:
        st.info("Selecione um exercício na lista acima para ver os detalhes.") 