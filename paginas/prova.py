import streamlit as st
import os
import json
# Importa funções auxiliares e de IA
from paginas.funcoes import (
    buscar_modulos, 
    formatar_nome_modulo, 
    buscar_licoes, 
    ler_licao,
    registrar_atividade_academica,
    registrar_acao_usuario
)
# Importa apenas a função de gerar prova do llms
from paginas.llms import gerar_prova_simulada

st.title("📝 Avaliação AI")
st.info("Selecione um módulo para gerar uma prova simulada sobre os tópicos abordados.")

# --- Seleção do Módulo ---
diretorio_base_aulas = 'aulas' 
modulos = buscar_modulos(diretorio_base_aulas)

if not modulos:
    st.warning("Nenhum módulo de aula encontrado. Verifique a organização da pasta 'aulas'.")
else:
    modulo_selecionado_nome_fmt = st.pills(
        ' ',
        modulos,
        format_func=formatar_nome_modulo,
        key="select_modulo_prova", label_visibility = "collapsed"
        )

    st.divider()

    # --- Geração e Exibição da Prova --- 
    if modulo_selecionado_nome_fmt:
        # Registra seleção do módulo
        registrar_atividade_academica(
            tipo="avaliacao",
            modulo=formatar_nome_modulo(modulo_selecionado_nome_fmt),
            detalhes={
                "acao": "selecao_modulo"
            }
        )
        
        # Inicializa estado para a prova do módulo
        if 'prova_modulo_atual' not in st.session_state:
            st.session_state.prova_modulo_atual = None
        if 'prova_gabarito' not in st.session_state:
            st.session_state.prova_gabarito = None
        if 'prova_submetida' not in st.session_state:
            st.session_state.prova_submetida = False
        if 'prova_respostas_aluno' not in st.session_state:
            st.session_state.prova_respostas_aluno = {}
            
        # Verifica se o módulo selecionado mudou para limpar a prova anterior
        if 'modulo_prova_anterior' not in st.session_state or st.session_state.modulo_prova_anterior != modulo_selecionado_nome_fmt:
            st.session_state.prova_modulo_atual = None
            st.session_state.prova_gabarito = None
            st.session_state.prova_submetida = False
            st.session_state.prova_respostas_aluno = {}
            st.session_state.modulo_prova_anterior = modulo_selecionado_nome_fmt

        if st.button(f"📝 Gerar Prova para Módulo: {formatar_nome_modulo(modulo_selecionado_nome_fmt)}", key="btn_gerar_prova", type="primary"):
            # Limpa estado antes de gerar nova prova
            st.session_state.prova_modulo_atual = None
            st.session_state.prova_gabarito = None
            st.session_state.prova_submetida = False
            st.session_state.prova_respostas_aluno = {}
            
            with st.spinner("Preparando material e gerando prova..."):
                # 1. Ler todas as lições do módulo selecionado
                diretorio_modulo = os.path.join(diretorio_base_aulas, modulo_selecionado_nome_fmt)
                licoes_modulo = buscar_licoes(diretorio_modulo)
                conteudo_concatenado = ""
                nomes_licoes = []
                if not licoes_modulo:
                    st.error(f"Nenhuma lição encontrada no módulo '{formatar_nome_modulo(modulo_selecionado_nome_fmt)}'. Impossível gerar prova.")
                else:
                    for nome_licao in licoes_modulo:
                        caminho_licao = os.path.join(diretorio_modulo, nome_licao)
                        conteudo = ler_licao(caminho_licao)
                        if conteudo:
                            conteudo_concatenado += f"\n\n--- CONTEÚDO DA LIÇÃO: {nome_licao} ---\n\n{conteudo}"
                            nomes_licoes.append(nome_licao.replace('.txt',''))
                    
                    if not conteudo_concatenado:
                         st.error("Não foi possível ler o conteúdo das lições neste módulo.")
                    else:
                        # 2. Chamar a função modularizada para gerar a prova
                        prova_data = gerar_prova_simulada(conteudo_concatenado, nomes_licoes)
                        
                        if prova_data: # Verifica se a função retornou dados válidos
                            st.session_state.prova_modulo_atual = prova_data.get("perguntas")
                            st.session_state.prova_gabarito = prova_data.get("gabarito")
                            st.session_state.prova_submetida = False
                            st.session_state.prova_respostas_aluno = {}
                            # Validação adicional (redundante se feita em llms.py, mas segura)
                            if st.session_state.prova_modulo_atual and st.session_state.prova_gabarito and len(st.session_state.prova_modulo_atual) == 5:
                                st.success("Prova Gerada! Responda abaixo.")
                                # Registra geração da prova
                                registrar_atividade_academica(
                                    tipo="avaliacao",
                                    modulo=formatar_nome_modulo(modulo_selecionado_nome_fmt),
                                    detalhes={
                                        "acao": "geracao_prova",
                                        "num_questoes": len(st.session_state.prova_modulo_atual)
                                    }
                                )
                            else:
                                st.error("Falha ao extrair perguntas ou gabarito da prova gerada.")
                                st.session_state.prova_modulo_atual = None # Garante reset
                        # Erros de API/JSON já são tratados e exibidos dentro da função gerar_prova_simulada
                        else:
                             st.session_state.prova_modulo_atual = None # Garante reset em caso de falha
        
        # --- Exibir Formulário da Prova --- 
        if st.session_state.prova_modulo_atual and not st.session_state.prova_submetida:
            st.subheader(f"Prova Simulado - Módulo: {formatar_nome_modulo(modulo_selecionado_nome_fmt)}")
            with st.form("prova_form"): 
                respostas_temp = {} 
                for pergunta in st.session_state.prova_modulo_atual:
                    numero_pergunta = pergunta['numero']
                    key_pergunta = f"prova_pergunta_{numero_pergunta}"
                    enunciado = pergunta['enunciado']
                    opcoes = pergunta['opcoes']
                    
                    resposta = st.radio(f"**{numero_pergunta}. {enunciado}**", options=opcoes, key=key_pergunta, index=None) 
                    respostas_temp[str(numero_pergunta)] = resposta 
                
                submitted = st.form_submit_button("Finalizar e Corrigir Prova", type="primary")
                
                if submitted:
                    if None in respostas_temp.values():
                        st.warning("Por favor, responda todas as questões antes de finalizar.")
                    else:
                        st.session_state.prova_respostas_aluno = respostas_temp
                        st.session_state.prova_submetida = True
                        st.rerun() # Recarrega para mostrar o resultado

        # --- Exibir Resultado da Prova --- 
        if st.session_state.prova_submetida and st.session_state.prova_modulo_atual and st.session_state.prova_gabarito:
            st.subheader(f"Resultado da Prova - Módulo: {formatar_nome_modulo(modulo_selecionado_nome_fmt)}")
            
            pontuacao = 0
            total_perguntas = len(st.session_state.prova_modulo_atual)
            
            for num_pergunta_str, resposta_correta in st.session_state.prova_gabarito.items():
                resposta_aluno = st.session_state.prova_respostas_aluno.get(num_pergunta_str)
                pergunta_atual = next((p for p in st.session_state.prova_modulo_atual if str(p['numero']) == num_pergunta_str), None)
                enunciado = pergunta_atual['enunciado'] if pergunta_atual else f"Questão {num_pergunta_str}"
                
                is_correct = (resposta_aluno == resposta_correta)
                if is_correct:
                    pontuacao += 1
                    st.markdown(f"✅ **{num_pergunta_str}. {enunciado}**")
                    st.success(f"   Sua resposta: {resposta_aluno} (Correta!)")
                else:
                    st.markdown(f"❌ **{num_pergunta_str}. {enunciado}**")
                    st.error(f"   Sua resposta: {resposta_aluno}")
                    st.info(f"   Resposta Correta: {resposta_correta}")
                st.markdown(" ") 
            
            st.divider()
            percentual = (pontuacao / total_perguntas) * 100
            st.metric(label="Sua Pontuação Final", value=f"{pontuacao}/{total_perguntas}", delta=f"{percentual:.1f}%")
            
            # Registra conclusão da prova
            registrar_atividade_academica(
                tipo="avaliacao",
                modulo=formatar_nome_modulo(modulo_selecionado_nome_fmt),
                detalhes={
                    "acao": "conclusao_prova",
                    "pontuacao": pontuacao,
                    "total_perguntas": total_perguntas,
                    "percentual_acerto": percentual,
                    "tempo_conclusao": None  # TODO: Implementar tracking de tempo
                }
            )
            
            if percentual == 100:
                st.balloons()
            elif percentual >= 70:
                st.success("Parabéns! Você foi bem.")
            elif percentual >= 50:
                st.warning("Resultado razoável, mas revise os pontos errados.")
            else:
                st.error("Recomendamos revisar o conteúdo deste módulo.")








