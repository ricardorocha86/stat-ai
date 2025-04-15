import pandas as pd
from datetime import datetime
import streamlit as st
from firebase_admin import firestore, credentials 
import firebase_admin
import os # Necessário para as funções abaixo
import re  # Necessário para as funções abaixo

# Nome da coleção principal de usuários definida como variável global
COLECAO_USUARIOS = "alunos-mata44-mat027-2025.1"

def inicializar_firebase():
    # Verifica se estamos em produção (Streamlit Cloud) ou desenvolvimento local
    if 'firebase' in st.secrets:
        cred = credentials.Certificate({
            "type": st.secrets.firebase.type,
            "project_id": st.secrets.firebase.project_id,
            "private_key_id": st.secrets.firebase.private_key_id,
            "private_key": st.secrets.firebase.private_key,
            "client_email": st.secrets.firebase.client_email,
            "client_id": st.secrets.firebase.client_id,
            "auth_uri": st.secrets.firebase.auth_uri,
            "token_uri": st.secrets.firebase.token_uri,
            "auth_provider_x509_cert_url": st.secrets.firebase.auth_provider_x509_cert_url,
            "client_x509_cert_url": st.secrets.firebase.client_x509_cert_url,
            "universe_domain": st.secrets.firebase.universe_domain
        })
    else:
        # Usa o arquivo local em desenvolvimento
        cred = credentials.Certificate("firebase-key.json")
        
    # Inicializa o Firebase apenas se ainda não foi inicializado
    try:
        firebase_admin.get_app() 
    except ValueError:
        firebase_admin.initialize_app(cred)

def login_usuario():
    """
    Registra ou atualiza dados do usuário no Firestore.
    Cria um novo registro se o usuário não existir, ou atualiza o último acesso se já existir.
    Retorna True se for o primeiro login, False caso contrário.
    """
    if not hasattr(st.experimental_user, 'email'):
        return False # Se não houver email, não tenta registrar o usuário
        
    db = firestore.client()
    doc_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email)
    doc = doc_ref.get()

    if not doc.exists:
        dados_usuario = {
            # Dados do Google Login
            "email": st.experimental_user.email,
            "nome_google": getattr(st.experimental_user, 'name', ''),
            "primeiro_nome_google": getattr(st.experimental_user, 'given_name', ''),
            "ultimo_nome_google": getattr(st.experimental_user, 'family_name', ''),
            "foto": getattr(st.experimental_user, 'picture', None),
            # Dados específicos do App (coletados no primeiro acesso)
            "nome_completo": "", 
            "matricula": "",
            "curso": "", # Farmácia ou Nutrição
            # Controle e Metadados
            "data_cadastro": datetime.now(),
            "ultimo_acesso": datetime.now(),
            "primeiro_acesso_concluido": False # Flag para o formulário inicial
        }
        doc_ref.set(dados_usuario)
        # Define um flag para mostrar a mensagem de boas-vindas (opcional agora)
        # st.session_state['show_welcome_message'] = True 
        registrar_acao_usuario("Cadastro", "Novo usuário registrado")
        if 'login_registrado' not in st.session_state:
             st.session_state['login_registrado'] = True # Marca como registrado para evitar loop
        return True # Indica que é o primeiro login
    else:
        doc_ref.update({"ultimo_acesso": datetime.now()})
        if 'login_registrado' not in st.session_state:
            registrar_acao_usuario("Login", "Usuário fez login")
            st.session_state['login_registrado'] = True
        return False # Indica que não é o primeiro login

def registrar_acao_usuario(acao: str, detalhes: str = ""):
    """
    Registra uma ação do usuário no Firestore.
    
    Args:
        acao: Nome da ação realizada
        detalhes: Detalhes adicionais da ação (opcional)
    """
    if not hasattr(st.experimental_user, 'email'):
        return  # Se não houver email, não registra a ação
        
    db = firestore.client()
    logs_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("logs")
    
    dados_log = {
        "acao": acao,
        "detalhes": detalhes,
        "data_hora": datetime.now()
    }
    
    logs_ref.add(dados_log)

def registrar_atividade_academica(tipo: str, modulo: str, detalhes: dict):
    """
    Registra uma atividade acadêmica específica do usuário.
    
    Args:
        tipo: Tipo da atividade (ex: 'aula', 'exercicio', 'avaliacao', 'simulado')
        modulo: Nome do módulo ou seção relacionada
        detalhes: Dicionário com detalhes específicos da atividade
            Exemplos de detalhes:
            - Para aulas: {"licao": "nome_licao", "tempo_estudo": "minutos"}
            - Para exercícios: {"questoes_total": 10, "acertos": 8}
            - Para avaliações: {"nota": 9.5, "tempo_prova": "minutos"}
    """
    if not hasattr(st.experimental_user, 'email'):
        return
        
    db = firestore.client()
    atividades_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("atividades_academicas")
    
    dados_atividade = {
        "tipo": tipo,
        "modulo": modulo,
        "detalhes": detalhes,
        "data_hora": datetime.now()
    }
    
    atividades_ref.add(dados_atividade)

def obter_idade(data_nascimento):
    """
    Calcula a idade a partir da data de nascimento.
    
    Args:
        data_nascimento: Data de nascimento do usuário
    
    Returns:
        int: Idade do usuário
    """
    if data_nascimento:
        hoje = datetime.now()
        idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
        return idade
    return None

def obter_perfil_usuario():
    """
    Obtém os dados de perfil do usuário atual do Firestore.
    
    Returns:
        dict: Dicionário com os dados do perfil do usuário ou None se não encontrado/erro.
    """
    if not hasattr(st.experimental_user, 'email'):
        return None
        
    db = firestore.client()
    doc_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email)
    try:
        doc = doc_ref.get()
        if doc.exists:
            dados = doc.to_dict()
            return {
                # Campos essenciais mantidos
                "email": dados.get("email", ""),
                "foto": dados.get("foto", ""), 
                # Novos campos específicos do App
                "nome_completo": dados.get("nome_completo", ""),
                "matricula": dados.get("matricula", ""),
                "curso": dados.get("curso", ""), 
                # Flag de controle
                "primeiro_acesso_concluido": dados.get("primeiro_acesso_concluido", False),
                # Campos derivados do Google (mantidos para referência, se útil)
                "nome_google": dados.get("nome_google", ""), 
                "primeiro_nome_google": dados.get("primeiro_nome_google", ""),
            }
        else:
            # Usuário logado mas sem registro no Firestore (situação anormal)
            st.error("Seu registro não foi encontrado no banco de dados. Contate o suporte.")
            return None 
    except Exception as e:
        print(f"Erro ao obter perfil para {st.experimental_user.email}: {e}")
        st.warning("Não foi possível carregar os dados do seu perfil.")
        return None

def atualizar_perfil_usuario(dados_perfil):
    """
    Atualiza os dados de perfil do usuário atual.
    
    Args:
        dados_perfil: Dicionário com os dados do perfil a serem atualizados
    
    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário
    """
    if not hasattr(st.experimental_user, 'email'):
        return False  # Retorna False se não houver email
        
    db = firestore.client()
    doc_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email)
    try:
        doc_ref.update(dados_perfil)
        return True
    except Exception as e:
        print(f"Erro ao atualizar perfil para {st.experimental_user.email}: {e}")
        st.error("Ocorreu um erro ao salvar suas informações. Tente novamente.")
        return False

# Funções para gerenciar os chats
def salvar_chat(nome_chat, mensagens):
    """
    Salva um chat no Firestore para o usuário atual.
    
    Args:
        nome_chat: Nome identificador do chat
        mensagens: Lista de mensagens do chat (cada mensagem é um dicionário)
    
    Returns:
        str: ID do chat salvo ou None em caso de erro
    """
    if not hasattr(st.experimental_user, 'email'):
        return None  # Retorna None se não houver email
        
    db = firestore.client()
    chat_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("chats")
    
    # Se não tiver nome, usa a data/hora como nome
    if not nome_chat:
        nome_chat = f"Chat de {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    try:
        # Verifica se já existe um chat com este nome
        query = chat_ref.where("nome", "==", nome_chat).limit(1).get()
        
        if len(query) > 0:
            # Atualiza o chat existente
            chat_id = query[0].id
            chat_ref.document(chat_id).update({
                "nome": nome_chat,
                "mensagens": mensagens, # Salva mensagens diretamente (sem avatar)
                "ultima_atualizacao": datetime.now()
            })
            return chat_id
        else:
            # Cria um novo chat
            novo_chat = {
                "nome": nome_chat,
                "mensagens": mensagens, # Salva mensagens diretamente (sem avatar)
                "data_criacao": datetime.now(),
                "ultima_atualizacao": datetime.now()
            }
            doc_ref = chat_ref.add(novo_chat)
            return doc_ref[1].id
    except Exception as e:
        print(f"Erro ao salvar chat para {st.experimental_user.email}: {e}")
        st.error("Não foi possível salvar o chat. Verifique sua conexão.")
        return None

def obter_chats():
    """
    Obtém todos os chats do usuário atual.
    
    Returns:
        list: Lista de dicionários, cada um representando um chat
    """
    if not hasattr(st.experimental_user, 'email'):
        return []  # Retorna lista vazia se não houver email
        
    db = firestore.client()
    chats_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("chats")
    try:
        docs = chats_ref.order_by("ultima_atualizacao", direction=firestore.Query.DESCENDING).stream()
        
        resultado = []
        for chat in docs:
            chat_data = chat.to_dict()
            chat_data["id"] = chat.id
            resultado.append(chat_data)
        return resultado
    except Exception as e:
        print(f"Erro ao obter chats para {st.experimental_user.email}: {e}")
        st.warning("Não foi possível carregar o histórico de chats.")
        return []

def obter_chat(chat_id):
    """
    Obtém um chat específico do usuário atual.
    
    Args:
        chat_id: ID do chat a ser carregado
    
    Returns:
        dict: Dicionário com os dados do chat ou None em caso de erro
    """
    if not hasattr(st.experimental_user, 'email'):
        return None  # Retorna None se não houver email
        
    db = firestore.client()
    chat_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("chats").document(chat_id)
    try:
        chat = chat_ref.get()
        if chat.exists:
            chat_data = chat.to_dict()
            chat_data["id"] = chat.id
            return chat_data
        else:
            st.warning("Chat não encontrado.")
            return None
    except Exception as e:
        print(f"Erro ao obter chat {chat_id} para {st.experimental_user.email}: {e}")
        st.warning("Não foi possível carregar os dados deste chat.")
        return None

def excluir_chat(chat_id):
    """
    Exclui um chat específico do usuário atual.
    
    Args:
        chat_id: ID do chat a ser excluído
    
    Returns:
        bool: True se a exclusão foi bem-sucedida, False caso contrário
    """
    if not hasattr(st.experimental_user, 'email'):
        return False  # Retorna False se não houver email
        
    db = firestore.client()
    chat_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("chats").document(chat_id)
    try:
        chat = chat_ref.get()
        if chat.exists:
            chat_ref.delete()
            return True
        else:
            # Não precisa de mensagem, a UI já vai atualizar
            return False
    except Exception as e:
        print(f"Erro ao excluir chat {chat_id} para {st.experimental_user.email}: {e}")
        st.error("Não foi possível excluir o chat.")
        return False

# --- Funções Auxiliares para Navegação de Aulas/Módulos ---

def buscar_modulos(diretorio_base):
    """Busca subdiretórios (módulos) no diretório base, ignorando os que começam com _."""
    try:
        # Lista diretórios e filtra os que não começam com _
        modulos_validos = [d for d in os.listdir(diretorio_base) 
                           if os.path.isdir(os.path.join(diretorio_base, d)) and not d.startswith('_')]
        return sorted(modulos_validos) # Ordena alfabeticamente (pelo prefixo numérico)
    except FileNotFoundError:
        st.error(f"Diretório de aulas não encontrado: {diretorio_base}")
        return []
    except Exception as e:
        st.error(f"Erro ao buscar módulos: {e}")
        return []

def extrair_numero_licao(nome_arquivo):
    """Extrai o número inicial do nome do arquivo da lição (ex: 'Lição 10...')."""
    match = re.match(r'^Lição\s+(\d+)', nome_arquivo) 
    if match:
        return int(match.group(1))
    # Tenta extrair número se não começar com "Lição"
    match_num_only = re.match(r'^(\d+)', nome_arquivo)
    if match_num_only:
        return int(match_num_only.group(1))
    return float('inf') # Retorna infinito se não encontrar número, para colocar no final

def buscar_licoes(diretorio_modulo):
    """Busca arquivos .txt (lições) em um diretório de módulo e ordena."""
    try:
        licoes = [f for f in os.listdir(diretorio_modulo) if f.endswith('.txt')]
        # Ordena numericamente baseado no início do nome ("Lição X")
        return sorted(licoes, key=extrair_numero_licao)
    except FileNotFoundError:
        # Não mostra erro aqui, pois pode ser chamado antes do diretório ser criado
        return [] 
    except Exception as e:
        st.error(f"Erro ao buscar lições em {diretorio_modulo}: {e}")
        return []

def ler_licao(arquivo_path):
    """Lê o conteúdo de um arquivo de lição.
    Retorna o conteúdo ou None em caso de erro.
    """
    try:
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # st.error(f"Erro: Arquivo da lição não encontrado em {arquivo_path}.") # Pode ser muito verboso
        print(f"WARN: Arquivo da lição não encontrado em {arquivo_path}.")
        return None
    except Exception as e:
        st.error(f"Erro ao ler arquivo {arquivo_path}: {e}")
        return None

def formatar_nome_modulo(nome_diretorio):
    """Formata o nome do diretório do módulo para exibição (ex: 1_Descritiva -> Descritiva)."""
    parts = nome_diretorio.split('_', 1)
    if len(parts) > 1:
        return parts[1].replace('_', ' ') # Substitui underscores por espaços
    return nome_diretorio # Retorna original se não seguir o padrão

def formatar_nome_licao(nome_arquivo):
    """Remove a extensão .txt do nome da lição.
    
    Args:
        nome_arquivo (str): O nome completo do arquivo da lição (ex: "Lição 1 - Intro.txt")
        
    Returns:
        str: O nome da lição sem a extensão .txt.
    """
    return nome_arquivo[:-4] if nome_arquivo.endswith('.txt') else nome_arquivo

# --- Fim Funções Auxiliares de Navegação ---










