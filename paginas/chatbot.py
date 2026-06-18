import streamlit as st
from openai import OpenAI 
from paginas.funcoes import (
    obter_perfil_usuario, 
    registrar_acao_usuario, 
    registrar_atividade_academica,
    salvar_chat, 
    obter_chats, 
    obter_chat, 
    excluir_chat,
    inicializar_firebase
)
from paginas.llms import gerar_titulo_chat
from datetime import datetime

# Inicializa o Firebase
inicializar_firebase() 

# Obtém o perfil e define o nome do usuário ANTES de usar no popover
perfil = obter_perfil_usuario()
# Usa o primeiro nome para a saudação, com fallback para o given_name do login ou 'Usuário'
nome_usuario = (
    perfil.get("primeiro_nome")
    or perfil.get("primeiro_nome_google")
    or getattr(st.user, 'given_name', 'Usuário')
)

# Verifica e exibe a mensagem de boas-vindas no primeiro login
if st.session_state.get('show_welcome_message', False):
    with st.popover("Bem-vindo(a)! 🎉", use_container_width=True):
        st.markdown(f"Olá, **{nome_usuario}**! Ficamos felizes em ter você por aqui.")
        st.markdown("Explore o chatbot e personalize sua experiência na página **Meu Perfil**.")
        st.button("Entendi!", use_container_width=True, key="welcome_close")
    # Remove o flag para não mostrar novamente
    del st.session_state['show_welcome_message']

# Configurações iniciais
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

# Define o avatar do usuário: usa a foto do perfil se for uma URL válida, senão usa o avatar padrão
user_picture = getattr(st.user, 'picture', None)
if user_picture and isinstance(user_picture, str) and user_picture.startswith(('http://', 'https://')):
    avatar_user = user_picture
else:
    avatar_user = 'arquivos/avatar_usuario.jpg'

# Define o avatar do assistente
avatar_assistant = 'arquivos/avatar_assistente.jpg'
MENSAGEM_INICIAL = 'Olá! Como posso te ajudar hoje?' # Mensagem inicial genérica

# Inicialização do histórico de mensagens e chat ativo
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "assistant",
            "content": MENSAGEM_INICIAL # Avatar não é mais armazenado na mensagem
        }
    ]

if 'chat_ativo_id' not in st.session_state:
    st.session_state.chat_ativo_id = None

if 'chat_ativo_nome' not in st.session_state:
    st.session_state.chat_ativo_nome = "Novo Chat"

# Sidebar com histórico de chats
with st.sidebar: 
    
    # Botão de novo chat
    if st.button("✨ Novo Chat", key="novo_chat", use_container_width=True, type="primary"):
        st.session_state.mensagens = [
            {
                "role": "assistant",
                "content": MENSAGEM_INICIAL # Avatar não é mais armazenado na mensagem
            }
        ]
        st.session_state.chat_ativo_id = None
        st.session_state.chat_ativo_nome = "Novo Chat"
        registrar_acao_usuario("Novo Chat", "Usuário iniciou um novo chat")
        st.rerun()
    
    # Exibir chats existentes
    chats = obter_chats() 
    #st.write("📜 **Chats Anteriores**")
    
    # CSS personalizado para alinhar botões à esquerda
    st.markdown("""
        <style>
        /* Estiliza os botões de chat anterior usando o prefixo da chave */
        [class*="st-key-chat_"] button {
            text-align: left !important;
            justify-content: flex-start !important;
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicia uma div com uma classe específica para os botões de chat
    st.markdown('<div class="chat-button-section">', unsafe_allow_html=True)
    
    if len(chats) == 0:
        st.info("Você ainda não tem conversas salvas!")
    
    for chat in chats:
        col1, col2 = st.columns([7, 1])
        with col1:
            if st.button(f"{chat['nome']}", key=f"chat_{chat['id']}", use_container_width=True):
                chat_data = obter_chat(chat['id'])
                if chat_data and 'mensagens' in chat_data:
                    st.session_state.mensagens = chat_data['mensagens']
                    st.session_state.chat_ativo_id = chat['id']
                    st.session_state.chat_ativo_nome = chat['nome']
                    registrar_acao_usuario("Abrir Chat", f"Usuário abriu o chat {chat['nome']}")
                    st.rerun()
        with col2:
            if st.button("🗑️", key=f"excluir_{chat['id']}"):
                excluir_chat(chat['id'])
                registrar_acao_usuario("Excluir Chat", f"Usuário excluiu o chat {chat['nome']}")
                # Se o chat excluído for o ativo, iniciar um novo chat
                if st.session_state.chat_ativo_id == chat['id']:
                    st.session_state.mensagens = [
                        {
                            "role": "assistant",
                            "content": MENSAGEM_INICIAL # Avatar não é mais armazenado na mensagem
                        }
                    ]
                    st.session_state.chat_ativo_id = None
                    st.session_state.chat_ativo_nome = "Novo Chat"
                st.rerun()
    
    # Fecha a div
    st.markdown('</div>', unsafe_allow_html=True)
 

# Exibição do histórico de mensagens
for mensagem in st.session_state.mensagens:
    role = mensagem["role"]
    # Define o avatar a ser exibido baseado no role, usando as variáveis globais corretas,
    # ignorando o valor 'avatar' potencialmente incorreto salvo na mensagem.
    if role == "user":
        display_avatar = avatar_user
    elif role == "assistant":
        display_avatar = avatar_assistant
    else:
        display_avatar = None # Caso haja algum outro role inesperado
        
    with st.chat_message(role, avatar=display_avatar):
        # Aplica as substituições para formato de matemática do Streamlit apenas nas mensagens do assistente
        if role == "assistant":
            display_content = mensagem["content"].replace('\\[', '$$').replace('\\]', '$$')\
                                               .replace('\\(', '$').replace('\\)', '$')
            st.markdown(display_content)
        else:
            st.write(mensagem["content"])

# Input e processamento de mensagens
prompt = st.chat_input(placeholder="Puxe papo com o chatbot...")

if prompt:
    # Registra a pergunta do usuário
    registrar_atividade_academica(
        tipo="chatbot",
        modulo="Professor AI",
        detalhes={
            "acao": "pergunta",
            "tamanho_pergunta": len(prompt),
            "chat_id": st.session_state.chat_ativo_id,
            "chat_nome": st.session_state.chat_ativo_nome
        }
    )
    
    # Adiciona mensagem do usuário
    st.session_state.mensagens.append({
        "role": "user",
        "content": prompt
    })
    
    # Mostra mensagem do usuário
    with st.chat_message("user", avatar=avatar_user):
        st.write(prompt)

    # Processa resposta do assistente
    with st.chat_message("assistant", avatar=avatar_assistant):
        try: # Adiciona try para capturar erros da API OpenAI
            # Prepara mensagens para a thread
            messages = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in st.session_state.mensagens
                if msg["role"] in ["user", "assistant"]
            ]
 
            INSTRUCOES = """
            Você é um assistente de professor de estatística que tem acesso a aulas e deve sempre consultar essas aulas pra responder as dúvidas dos alunos.
            É crucial que você utilize o "file_search" para buscar as informações relevantes disponíveis nas aulas.
            Responda sempre exageradamente com Emojis
            """
            with st.spinner("Pera ai...💭", show_time=True):
                response = client.responses.create(
                    input= messages,
                    model="gpt-4.1-mini",
                    instructions = INSTRUCOES,
                    tools=[{
                        "type": "file_search",
                        "vector_store_ids": [st.secrets["VECTOR_STORE_ID"]],
                        #  "max_num_results": 12,  
                        # "ranking_options": {
                        #         "score_threshold": 0.25
                        #    }
                    }]
                )

                # Extract annotations from the response
                annotations = []
                retrieved_files = set()
                response_text = ""
                
                # Verifica se a resposta tem o formato esperado antes de acessar os índices
                if response.output and len(response.output) > 1 and response.output[1].content and len(response.output[1].content) > 0:
                    try:
                        annotations = response.output[1].content[0].annotations
                        retrieved_files = set([result.filename for result in annotations])
                        response_text = response.output[1].content[0].text
                    except (AttributeError, IndexError, TypeError) as e:
                        print(f"Erro ao extrair dados da resposta da API: {e}")
                        print(f"Estrutura da resposta: {response.output}")
                        # Tenta pegar a resposta principal de outra forma, se possível
                        if response.output and len(response.output) > 0 and response.output[0].content and len(response.output[0].content) > 0:
                           try:
                               response_text = response.output[0].content[0].text
                               print("Usando texto de response.output[0] como fallback.")
                           except (AttributeError, IndexError, TypeError):
                               pass # Mantém response_text vazio se falhar também
                        if not response_text: # Se ainda não conseguiu texto
                             response_text = "Desculpe, não consegui processar a resposta corretamente. 🤔"

                elif response.output and len(response.output) > 0 and response.output[0].content and len(response.output[0].content) > 0:
                     # Caso comum onde a resposta principal está em output[0]
                     try:
                         response_text = response.output[0].content[0].text
                     except (AttributeError, IndexError, TypeError) as e:
                         print(f"Erro ao extrair dados de response.output[0]: {e}")
                         response_text = "Desculpe, tive um problema ao processar a resposta. 😕"
                else:
                    print(f"Formato inesperado da resposta da API: {response.output}")
                    response_text = "Não recebi uma resposta válida do assistente. 🤷‍♂️"

                # Build the reference string if any files were retrieved
                if retrieved_files:
                    references = "\n\n --- \n**Referências:**\n" + "\n".join(f"- {filename[:-4]}" for filename in retrieved_files)
                else:
                    references = ""

                # Create the final string
                final_output = response_text + references

                assistant_reply = final_output
                st.write(assistant_reply.replace(r"\[", "$$")
                  .replace(r"\]", "$$")
                  .replace(r"\(", "$")
                  .replace(r"\)", "$"))
                

            # # Cria e processa a thread
            # thread = client.beta.threads.create(messages=messages)
            
            # with client.beta.threads.runs.stream(
            #     thread_id=thread.id,
            #     assistant_id=st.secrets["ASSISTENTE"] # Usa um único ID de assistente definido nos secrets
            # ) as stream:
            #     assistant_reply = ""
            #     message_placeholder = st.empty()
                
            #     for event in stream:
            #         if event.event == 'thread.message.delta':
            #             delta = event.data.delta.content[0].text.value
            #             assistant_reply += delta
            #             # Aplica as substituições para formato de matemática do Streamlit
            #             display_reply = assistant_reply.replace('\\[', '$$').replace('\\]', '$$')\
            #                                      .replace('\\(', '$').replace('\\)', '$')
            #             message_placeholder.markdown(display_reply)
            #             #time.sleep(0.01)
                
                # Adiciona resposta AO HISTÓRICO com a formatação ORIGINAL (sem replace)
            st.session_state.mensagens.append({
                    "role": "assistant",
                    "content": assistant_reply
                })
                
                # Log e salvamento do chat
            registrar_acao_usuario("Conversa com Chatbot", {'prompt': prompt, 'resposta': assistant_reply})
                
                # Salva o chat após cada interação
            if len(st.session_state.mensagens) > 1:  # Se há mais que a mensagem inicial
                if not st.session_state.chat_ativo_id:  # Se é um novo chat
                    # Gera um título para o novo chat
                    novo_titulo = gerar_titulo_chat(st.session_state.mensagens)
                    chat_id = salvar_chat(novo_titulo, st.session_state.mensagens)
                    st.session_state.chat_ativo_id = chat_id
                    st.session_state.chat_ativo_nome = novo_titulo
                    
                    # # Registra criação do novo chat
                    # registrar_atividade_academica(
                    #     tipo="chatbot",
                    #     modulo="Professor AI",
                    #     detalhes={
                    #         "acao": "novo_chat",
                    #         "chat_id": chat_id,
                    #         "chat_nome": novo_titulo
                    #     }
                    # )
               #else:  # Se é um chat existente
                    #salvar_chat(st.session_state.chat_ativo_nome, st.session_state.mensagens, st.session_state.chat_ativo_id)
                    
                    # Registra atualização do chat
                    # registrar_atividade_academica(
                    #     tipo="chatbot",
                    #     modulo="Professor AI",
                    #     detalhes={
                    #         "acao": "atualizacao_chat",
                    #         "chat_id": st.session_state.chat_ativo_id,
                    #         "chat_nome": st.session_state.chat_ativo_nome,
                    #         "num_mensagens": len(st.session_state.mensagens)
                    #     }
                    # )

                st.rerun()  # Atualiza a interface após salvar

        # Trata erros específicos da API OpenAI (agora com indentação correta)
        except Exception as e:
             print(f"Erro na chamada OpenAI: {e}")
             st.error(f"Ocorreu um erro ao comunicar com o assistente: {e}. Tente novamente.")
             # Remove a última mensagem (resposta com erro) do histórico para não poluir
             if st.session_state.mensagens and st.session_state.mensagens[-1]["role"] == "assistant":
                 st.session_state.mensagens.pop()
             # Registra erro no chat
             registrar_atividade_academica(
                 tipo="chatbot",
                 modulo="Professor AI",
                 detalhes={
                     "acao": "erro",
                     "erro": str(e),
                     "chat_id": st.session_state.chat_ativo_id,
                     "chat_nome": st.session_state.chat_ativo_nome
                 }
             )
