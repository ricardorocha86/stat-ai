import streamlit as st
import os
import re
import json # Importa a biblioteca JSON
# Adicionado: Importa funções de navegação e IA modularizadas
from paginas.funcoes import buscar_modulos, formatar_nome_modulo, buscar_licoes, ler_licao, formatar_nome_licao, registrar_atividade_academica, registrar_acao_usuario # formatar_nome_licao pode ser redundante agora
from paginas.llms import (
    gerar_exercicios_licao,
    gerar_insights_licao,
    gerar_quiz_licao,
    gerar_flashcards_licao 
)

# --- Funções Auxiliares ---

def st_markdown_with_images(markdown_string, base_aula_dir):
    """Renderiza markdown que pode conter links locais para imagens."""
    parts = re.split(r'!\[(.*?)\]\((.*?)\)', markdown_string)
    for i, part in enumerate(parts):
        if i % 3 == 0:
            st.markdown(part, unsafe_allow_html=True)
        elif i % 3 == 1:
            alt_text = part # Texto alternativo da imagem (não usado por padrão)
        else:
            image_path_md = part # Path como está escrito no markdown

            # Normaliza separadores para comparação e construção do caminho
            normalized_image_path_md = image_path_md.replace('\\', '/')
            normalized_base_dir = base_aula_dir.replace('\\', '/')

            # Verifica se o caminho no markdown JÁ inclui o nome do diretório base
            if normalized_image_path_md.startswith(normalized_base_dir + '/'):
                 # Assume que o caminho no markdown está correto em relação à raiz do workspace
                 full_image_path = image_path_md 
            else:
                 # Assume que o caminho no markdown é relativo AO diretório base das aulas
                 full_image_path = os.path.join(base_aula_dir, image_path_md)

            # Verifica a existência e exibe
            if os.path.exists(full_image_path):
                st.image(full_image_path)
            else:
                st.warning(f"Imagem não encontrada: {full_image_path}")
                # st.warning(f" (Debug: Base='{base_aula_dir}', PathMD='{image_path_md}')\") # Linha de debug opcional

# --- Lógica Principal (Seleção de Módulo/Lição) --- 
diretorio_base_aulas = 'aulas'
modulos = buscar_modulos(diretorio_base_aulas)

conteudo_licao_selecionada = ""
licao_selecionada_nome = ""

if not modulos:
    st.warning("Nenhum módulo de aula encontrado. Verifique se os subdiretórios foram criados corretamente dentro da pasta 'aulas'.")
else:
    # --- Seleção de Módulo e Lição em Colunas ---
    col1, col2 = st.columns([1,2])

    with col1:
        # Usamos st.selectbox para permitir a definição de um índice padrão.
        # O padrão é o último módulo na lista (o mais recente).
        modulo_selecionado_nome_fmt = st.selectbox(
            'Unidade:',
            modulos, 
            index=len(modulos) - 1, # Define o último módulo como padrão
            format_func=formatar_nome_modulo,
            key="select_modulo_main"
        )

    # Busca as lições baseadas no módulo selecionado
    diretorio_modulo_selecionado = os.path.join(diretorio_base_aulas, modulo_selecionado_nome_fmt)
    licoes_no_modulo = buscar_licoes(diretorio_modulo_selecionado)
    licao_selecionada_nome = "" # Inicializa a variável

    with col2:
        if not licoes_no_modulo:
            st.warning("Nenhuma lição encontrada neste módulo.")
        else:
            # O seletor de lição é populado com base no módulo escolhido.
            # O padrão é a primeira lição da lista.
            licao_selecionada_nome = st.selectbox(
                'Aula:',
                licoes_no_modulo,
                format_func=formatar_nome_licao,
                key="select_licao_main",
                index=0 # Define a primeira aula como padrão
            )

    if licao_selecionada_nome:
        caminho_licao = os.path.join(diretorio_modulo_selecionado, licao_selecionada_nome)
        conteudo_licao_selecionada = ler_licao(caminho_licao)
        # Registra acesso à lição
        registrar_atividade_academica(
            tipo="aula",
            modulo=formatar_nome_modulo(modulo_selecionado_nome_fmt),
            detalhes={
                "licao": formatar_nome_licao(licao_selecionada_nome),
                "acao": "visualizacao"
            }
        )

# --- Exibição do Conteúdo da Lição ---
if conteudo_licao_selecionada: 
    # Renderiza o conteúdo, passando o diretório base para resolver imagens
    st_markdown_with_images(conteudo_licao_selecionada, diretorio_base_aulas) 
   
    # --- Abas de IA ---
    st.divider()
    # Adiciona as novas abas
    abas_ia = ['Exercícios AI', 'Lista de Insights AI', 'Quiz AI', 'Flashcards AI']
    aba_exercicios, aba_insights, aba_quiz, aba_flashcards = st.tabs(abas_ia)

    # --- Aba de Exercícios ---
    with aba_exercicios:
        st.header(abas_ia[0]) 
        if st.button('✨ Gerar Lista de Exercícios desta Lição', key="btn_exercicios", type='primary'): 
            if not conteudo_licao_selecionada or conteudo_licao_selecionada.startswith("Erro:"):
                st.error("Não é possível gerar exercícios sem o conteúdo da lição.")
            else:
                with st.spinner("Gerando exercícios..."): # Adiciona spinner
                    stream = gerar_exercicios_licao(conteudo_licao_selecionada)
                    if stream:
                        with st.chat_message("assistant", avatar='🐵'):
                            response = st.write_stream(stream)
                            # Registra geração de exercícios
                            registrar_atividade_academica(
                                tipo="exercicio",
                                modulo=formatar_nome_modulo(modulo_selecionado_nome_fmt),
                                detalhes={
                                    "licao": formatar_nome_licao(licao_selecionada_nome),
                                    "acao": "geracao_exercicios"
                                }
                            )
                    # Erros já são tratados dentro da função gerar_exercicios_licao

    # --- Aba de Insights ---
    with aba_insights:
        st.header(abas_ia[1]) 
        if st.button('✨ Gerar Lista de Insights desta Lição', key="btn_insights", type='primary'): 
            if not conteudo_licao_selecionada or conteudo_licao_selecionada.startswith("Erro:"):
                st.error("Não é possível gerar insights sem o conteúdo da lição.")
            else:
                 with st.spinner("Gerando insights..."):
                    stream = gerar_insights_licao(conteudo_licao_selecionada)
                    if stream:
                        with st.chat_message("assistant", avatar='💡'): # Avatar alterado
                            response = st.write_stream(stream)
                            # Registra geração de insights
                            registrar_atividade_academica(
                                tipo="estudo",
                                modulo=formatar_nome_modulo(modulo_selecionado_nome_fmt),
                                detalhes={
                                    "licao": formatar_nome_licao(licao_selecionada_nome),
                                    "acao": "geracao_insights"
                                }
                            )
                    # Erros já são tratados dentro da função

    # --- Aba: Quiz AI ---
    with aba_quiz:
        st.header(abas_ia[2])

        # Inicializa o estado para o quiz se não existir
        if 'quiz_gerado' not in st.session_state:
            st.session_state.quiz_gerado = None
        if 'quiz_respostas_corretas' not in st.session_state:
            st.session_state.quiz_respostas_corretas = None
        if 'quiz_submetido' not in st.session_state:
            st.session_state.quiz_submetido = False
        if 'respostas_aluno' not in st.session_state:
            st.session_state.respostas_aluno = {}
        if 'quiz_generation_count' not in st.session_state: # NOVO: Contador para a key do formulário
            st.session_state.quiz_generation_count = 0

        # Botão para gerar um NOVO quiz
        if st.button("❓ Gerar Novo Quiz", key="btn_gerar_quiz", type="secondary"):
            if not conteudo_licao_selecionada or conteudo_licao_selecionada.startswith("Erro:"):
                st.error("Não é possível gerar quiz sem o conteúdo da lição.")
            else:
                st.session_state.quiz_generation_count += 1 # NOVO: Incrementar contador
                st.session_state.quiz_gerado = None # Limpa quiz anterior
                st.session_state.quiz_respostas_corretas = None
                st.session_state.quiz_submetido = False
                st.session_state.respostas_aluno = {}
                
                with st.spinner("Gerando quiz..."): 
                    quiz_data = gerar_quiz_licao(conteudo_licao_selecionada)
                    if quiz_data: # Verifica se a função retornou dados válidos
                        st.session_state.quiz_gerado = quiz_data.get("perguntas")
                        
                        raw_gabarito = quiz_data.get("gabarito")
                        if raw_gabarito and isinstance(raw_gabarito, dict):
                            st.session_state.quiz_respostas_corretas = {str(k): v for k, v in raw_gabarito.items()}
                        else:
                            st.session_state.quiz_respostas_corretas = None
                        
                        if st.session_state.quiz_gerado and st.session_state.quiz_respostas_corretas:
                             st.success("Quiz gerado! Responda abaixo.")
                        else:
                             st.error("Falha ao extrair perguntas ou gabarito do quiz gerado.")
                             st.session_state.quiz_gerado = None # Garante reset
                             st.session_state.quiz_respostas_corretas = None # Garante reset
                    # Erros de API/JSON decode já são tratados e exibidos dentro da função gerar_quiz_licao
                    else: # quiz_data é None (falha na geração)
                         st.session_state.quiz_gerado = None # Garante reset em caso de falha
                         st.session_state.quiz_respostas_corretas = None # Garante reset em caso de falha

        # Exibe o formulário do quiz se ele foi gerado e não submetido
        if st.session_state.quiz_gerado and not st.session_state.quiz_submetido:
            st.markdown("--- ")
            st.subheader("Responda o Quiz:")
            # NOVO: Usar o contador na key do formulário
            with st.form(f"quiz_form_{st.session_state.quiz_generation_count}"): 
                respostas_temp = {} 
                for pergunta in st.session_state.quiz_gerado:
                    numero_pergunta = pergunta['numero']
                    key_pergunta = f"pergunta_{numero_pergunta}"
                    enunciado = pergunta['enunciado']
                    opcoes = pergunta['opcoes']
                    
                    # Usa st.radio para as respostas
                    resposta = st.radio(f"**{numero_pergunta}. {enunciado}**", options=opcoes, key=key_pergunta, index=None) # index=None para não ter pré-seleção
                    respostas_temp[str(numero_pergunta)] = resposta # Guarda resposta temporária
                
                submitted = st.form_submit_button("Verificar Respostas", type="primary")
                
                if submitted:
                    # Verifica se todas as perguntas foram respondidas
                    if None in respostas_temp.values():
                        st.warning("Por favor, responda todas as perguntas antes de verificar.")
                    else:
                        st.session_state.respostas_aluno = respostas_temp
                        st.session_state.quiz_submetido = True
                        
                        # Calcula pontuação antes do rerun
                        pontuacao = sum(1 for num, resp in respostas_temp.items() 
                                      if resp == st.session_state.quiz_respostas_corretas.get(num))
                        total_perguntas = len(st.session_state.quiz_gerado)
                        
                        # Registra conclusão do quiz
                        registrar_atividade_academica(
                            tipo="quiz",
                            modulo=formatar_nome_modulo(modulo_selecionado_nome_fmt),
                            detalhes={
                                "licao": formatar_nome_licao(licao_selecionada_nome),
                                "pontuacao": pontuacao,
                                "total_perguntas": total_perguntas,
                                "percentual_acerto": (pontuacao / total_perguntas) * 100
                            }
                        )
                        
                        st.rerun()

        # Exibe o resultado após submissão
        if st.session_state.quiz_submetido and st.session_state.quiz_gerado and st.session_state.quiz_respostas_corretas:
            st.markdown("--- ")
            st.subheader("Resultado do Quiz:")
            
            pontuacao = 0
            total_perguntas = len(st.session_state.quiz_gerado)
            
            for num_pergunta_str, resposta_correta in st.session_state.quiz_respostas_corretas.items():
                resposta_aluno = st.session_state.respostas_aluno.get(num_pergunta_str)
                
                # Encontra a pergunta correspondente para exibir o enunciado
                pergunta_atual = next((p for p in st.session_state.quiz_gerado if str(p['numero']) == num_pergunta_str), None)
                enunciado = pergunta_atual['enunciado'] if pergunta_atual else f"Pergunta {num_pergunta_str}"
                
                is_correct = (resposta_aluno == resposta_correta)
                if is_correct:
                    pontuacao += 1
                    st.markdown(f"✅ **{num_pergunta_str}. {enunciado}**")
                    st.success(f"   Sua resposta: {resposta_aluno} (Correta!)")
                else:
                    st.markdown(f"❌ **{num_pergunta_str}. {enunciado}**")
                    st.error(f"   Sua resposta: {resposta_aluno}")
                    st.info(f"   Resposta Correta: {resposta_correta}")
                st.markdown(" ") # Espaçamento
            
            st.markdown("--- ")
            percentual = (pontuacao / total_perguntas) * 100
            st.metric(label="Sua Pontuação Final", value=f"{pontuacao}/{total_perguntas}", delta=f"{percentual:.1f}%")
            
            if percentual == 100:
                st.balloons()
            elif percentual >= 70:
                st.success("Ótimo trabalho!")
            elif percentual >= 50:
                st.warning("Continue estudando!")
            else:
                st.error("Você precisa revisar esta lição.")

    # --- Aba: Flashcards AI ---
    with aba_flashcards:
        st.header(abas_ia[3])

        # Inicializa o estado para os flashcards
        if 'flashcards_gerados' not in st.session_state:
            st.session_state.flashcards_gerados = None
        if 'flashcard_index' not in st.session_state:
            st.session_state.flashcard_index = 0
        if 'flashcard_virado' not in st.session_state:
            st.session_state.flashcard_virado = False

        # Estilo CSS para os flashcards
        st.markdown("""
        <style>
        .flashcard-container {
            perspective: 1000px; /* Perspectiva para efeito 3D */
            margin: 20px auto;
            width: 80%;
            max-width: 500px;
            height: 250px;
        }
        .flashcard {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-radius: 15px;
        }
        .flashcard.flipped {
            transform: rotateY(180deg);
        }
        .flashcard-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden; /* Esconde o lado de trás */
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
            border-radius: 15px;
            font-size: 18px;
        }
        .flashcard-front {
            background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%); /* Tons de azul claro */
            color: #00796b; /* Verde azulado escuro */
        }
        .flashcard-back {
            background: linear-gradient(135deg, #fffde7 0%, #fff9c4 100%); /* Tons de amarelo claro */
            color: #f57f17; /* Laranja escuro */
            transform: rotateY(180deg);
        }
        .flashcard-nav {
            display: flex;
            justify-content: space-around;
            margin-top: 15px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Botão para gerar NOVOS flashcards
        if st.button("📇 Gerar Flashcards", key="btn_gerar_flashcards", type="secondary"):
            if not conteudo_licao_selecionada or conteudo_licao_selecionada.startswith("Erro:"):
                st.error("Não é possível gerar flashcards sem o conteúdo da lição.")
            else:
                st.session_state.flashcards_gerados = None # Limpa anteriores
                st.session_state.flashcard_index = 0
                st.session_state.flashcard_virado = False
                with st.spinner("Gerando flashcards..."):
                    lista_flashcards = gerar_flashcards_licao(conteudo_licao_selecionada)
                    if lista_flashcards: # Verifica se a função retornou uma lista válida
                        st.session_state.flashcards_gerados = lista_flashcards
                        st.session_state.flashcard_index = 0
                        st.session_state.flashcard_virado = False
                        st.success(f"{len(st.session_state.flashcards_gerados)} flashcards gerados!")
                    else:
                        # Mensagem se a lista for vazia ou None (erro já tratado na função)
                        if lista_flashcards is not None: # Distingue lista vazia de erro
                             st.warning("A IA não conseguiu gerar flashcards para esta lição.")
                        st.session_state.flashcards_gerados = None # Garante reset

        # Exibe o flashcard atual se houver flashcards gerados
        if st.session_state.flashcards_gerados:
            total_cards = len(st.session_state.flashcards_gerados)
            current_index = st.session_state.flashcard_index
            card_data = st.session_state.flashcards_gerados[current_index]
            
            # Container do flashcard com classe para CSS e lógica de virar
            flip_class = " flipped" if st.session_state.flashcard_virado else ""
            st.markdown(f'<div class="flashcard-container"><div class="flashcard{flip_class}">'
                        f'<div class="flashcard-face flashcard-front">{card_data["frente"]}</div>'
                        f'<div class="flashcard-face flashcard-back">{card_data["verso"]}</div>'
                        f'</div></div>', unsafe_allow_html=True)

            # Botões de navegação e virar (Layout ajustado)
            col_prev, col_flip, col_next = st.columns([1, 2, 1]) # 3 Colunas: Laterais menores, centro maior
            
            with col_prev:
                 # Botão Anterior (desabilitado no primeiro card)
                if st.button("⬅️ Anterior", key="prev_card", disabled=current_index == 0, use_container_width=True):
                    st.session_state.flashcard_index -= 1
                    st.session_state.flashcard_virado = False # Desvira ao mudar
                    st.rerun()
            
            with col_flip:
                if st.button("🔄 Virar Card", key="flip_card", use_container_width=True):
                     st.session_state.flashcard_virado = not st.session_state.flashcard_virado
                     st.rerun()
            
            with col_next:
                 # Botão Próximo (desabilitado no último card)
                 if st.button("Próximo ➡️", key="next_card", disabled=current_index == total_cards - 1, use_container_width=True):
                     st.session_state.flashcard_index += 1
                     st.session_state.flashcard_virado = False # Desvira ao mudar
                     st.rerun()
            
            # Contador abaixo dos botões e centralizado
            st.markdown(f'<p style="text-align: center; color: #555; margin-top: 10px;">Card {current_index + 1} de {total_cards}</p>', unsafe_allow_html=True)
                 
            # st.markdown('</div>', unsafe_allow_html=True) # Fecha flashcard-nav -> Removido pois não é mais necessário
        elif st.session_state.flashcards_gerados is not None: # Se tentou gerar mas falhou ou veio vazio
            st.info("Clique em 'Gerar Flashcards' para começar.")

elif not modulos:
    # Mensagem já exibida acima se nenhum módulo foi encontrado
    pass 
else: 
    # Caso nenhum módulo ou lição seja selecionado (ou não haja lições no módulo)
    st.info("Selecione um módulo e uma lição na barra lateral para visualizar o conteúdo.")


