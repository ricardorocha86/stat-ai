import streamlit as st
import datetime
from firebase_admin import firestore
from paginas.funcoes import registrar_acao_usuario, registrar_atividade_academica, obter_perfil_usuario
import uuid
import base64
import io
import os

# Título da página
st.title("💬 Fórum de Discussão")

# CSS personalizado para os posts
st.markdown("""
<style>
.post-container {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    width: 100%;
    position: relative;
}

.post-container:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    transform: translateY(-2px);
    transition: all 0.3s ease;
}

.post-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.author-img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
    object-fit: cover;
}

.author-name {
    font-weight: bold;
    margin: 0;
    color: #2C3E50;
}

.post-date {
    font-size: 0.8em;
    color: #7F8C8D;
    margin-left: auto;
}

.post-content {
    margin-bottom: 15px;
    word-wrap: break-word;
}

.post-image {
    max-width: 100%;
    border-radius: 8px;
    margin-top: 10px;
    margin-bottom: 15px;
}

.like-section {
    position: absolute;
    right: 20px;
    bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    font-size: 0.9em;
    color: #7F8C8D;
}

.like-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #7F8C8D;
    display: flex;
    align-items: center;
    padding: 5px 10px;
    border-radius: 4px;
    transition: all 0.2s ease;
}

.like-btn:hover {
    background-color: #f1f1f1;
    transform: scale(1.1);
}

.like-btn.active {
    color: #3498db;
}

.like-count {
    margin-left: 5px;
}
</style>
""", unsafe_allow_html=True)

# Função para obter posts do fórum
def obter_posts_forum():
    db = firestore.client()
    posts_ref = db.collection("forum-posts").order_by("data_criacao", direction=firestore.Query.DESCENDING)
    
    try:
        posts = []
        for doc in posts_ref.stream():
            post_data = doc.to_dict()
            post_data["id"] = doc.id
            posts.append(post_data)
        return posts
    except Exception as e:
        st.error(f"Erro ao carregar posts: {e}")
        return []

# Função para criar um novo post
def criar_post(texto, imagem=None):
    if not texto and not imagem:
        return False
    
    perfil = obter_perfil_usuario()
    if not perfil:
        st.error("Não foi possível obter seu perfil. Tente novamente mais tarde.")
        return False
    
    db = firestore.client()
    post_data = {
        "texto": texto,
        "autor_email": getattr(st.user, "email", "local@localhost"),
        "autor_nome": perfil.get("nome_completo") or perfil.get("nome_google", "Usuário"),
        "autor_foto": perfil.get("foto", ""),
        "data_criacao": datetime.datetime.now(),
        "likes": 0,
        "usuarios_like": []
    }
    
    # Se houver imagem, converter para base64 e salvar como string simples (não aninhada)
    if imagem is not None:
        try:
            # Verificar o tamanho da imagem (limitar a 1MB)
            img_bytes = imagem.getvalue()
            img_size = len(img_bytes)
            
            if img_size > 1000000:  # 1MB em bytes
                st.warning("A imagem é muito grande (máximo 1MB). Redimensione-a antes de enviar.")
                return False
                
            # Converter para base64 como string simples
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            # Armazenar como campos separados (não aninhados)
            post_data["imagem_id"] = str(uuid.uuid4())
            post_data["imagem_base64"] = img_base64
            post_data["imagem_tipo"] = imagem.type
            
        except Exception as e:
            st.error(f"Erro ao processar imagem: {e}")
            # Continuar sem a imagem em caso de erro
    
    try:
        # Adiciona o post e obtém a referência
        post_ref = db.collection("forum-posts").add(post_data)
        
        # Registra a criação do post
        registrar_atividade_academica(
            tipo="forum",
            modulo="Fórum de Discussão",
            detalhes={
                "acao": "criar_post",
                "post_id": post_ref[1].id,
                "tamanho_texto": len(texto),
                "tem_imagem": imagem is not None
            }
        )
        
        return True
    except Exception as e:
        st.error(f"Erro ao criar post: {e}")
        return False

# Função para dar/remover like em um post
def alternar_like(post_id):
    db = firestore.client()
    post_ref = db.collection("forum-posts").document(post_id)
    
    try:
        post = post_ref.get()
        if not post.exists:
            return False
        
        post_data = post.to_dict()
        usuarios_like = post_data.get("usuarios_like", [])
        email_usuario = getattr(st.user, "email", "local@localhost")
        
        # Alternar o like
        if email_usuario in usuarios_like:
            usuarios_like.remove(email_usuario)
            post_ref.update({
                "likes": firestore.Increment(-1),
                "usuarios_like": usuarios_like
            })
            # Registra remoção do like
            registrar_atividade_academica(
                tipo="forum",
                modulo="Fórum de Discussão",
                detalhes={
                    "acao": "remover_like",
                    "post_id": post_id
                }
            )
        else:
            usuarios_like.append(email_usuario)
            post_ref.update({
                "likes": firestore.Increment(1),
                "usuarios_like": usuarios_like
            })
            # Registra adição do like
            registrar_atividade_academica(
                tipo="forum",
                modulo="Fórum de Discussão",
                detalhes={
                    "acao": "adicionar_like",
                    "post_id": post_id
                }
            )
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar like: {e}")
        return False

# Input para criar novo post
with st.container():
    post_input = st.chat_input(
        "Escreva sua mensagem para o fórum...",
       # accept_file=True,
       # file_type=["png", "jpg", "jpeg"]
    )
    
    # Processar input do chat (texto e/ou imagem)
    if post_input:
        texto = post_input.text if hasattr(post_input, "text") else post_input
        imagem = None
        
        # Verificar se tem arquivos anexados
        if hasattr(post_input, "files") and post_input.files:
            imagem = post_input.files[0]  # Pegar apenas o primeiro arquivo
        
        if texto or imagem:
            if criar_post(texto, imagem):
                st.success("Post criado com sucesso!")
                # Recarregar a página para exibir o novo post
                st.rerun()

# Exibir posts existentes
posts = obter_posts_forum()

if not posts:
    st.info("Nenhum post encontrado. Seja o primeiro a postar!")
else:
    # Exibir cada post em sequência
    for post in posts:
        # Criar colunas para o post e o botão de like
        col_post, col_like = st.columns([6, 1], gap="small")
        
        with col_post:
            # Criar um container para o post com estilo personalizado
            with st.container():
                post_id = post["id"]
                
                # Verificar se o usuário atual deu like neste post
                usuario_deu_like = getattr(st.user, "email", "local@localhost") in post.get("usuarios_like", [])
                
                # Preparar a URL da foto do autor - usar serviço externo como fallback garantido
                autor_nome = post.get('autor_nome', 'Usuário')
                autor_foto = post.get('autor_foto', '')
                
                # Se não tiver foto, usar diretamente serviço externo de avatar
                if not autor_foto or autor_foto.strip() == "":
                    avatar_url = f"https://ui-avatars.com/api/?name={autor_nome.replace(' ', '+')}&background=random&size=128"
                else:
                    avatar_url = autor_foto
                
                # Início do HTML do cabeçalho do post - sem onerror para simplificar
                st.markdown(f"""
                <div class="post-container" style="width: 100%; box-sizing: border-box;">
                    <div class="post-header" style="display: flex; align-items: center; margin-bottom: 10px;">
                        <img src="{avatar_url}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px; object-fit: cover;">
                        <p style="font-weight: bold; margin: 0; color: #2C3E50;">{autor_nome}</p>
                        <span style="font-size: 0.8em; color: #7F8C8D; margin-left: auto;">{post.get('data_criacao').strftime('%d/%m/%Y às %H:%M')}</span>
                    </div>
                    <div style="margin-bottom: 10px; word-wrap: break-word;">
                        {post.get('texto', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Exibir imagem se existir - verificar os campos individuais em vez de aninhados
                if "imagem_base64" in post and post["imagem_base64"]:
                    try:
                        img_base64 = post["imagem_base64"]
                        img_bytes = base64.b64decode(img_base64)
                        img_io = io.BytesIO(img_bytes)
                        st.image(img_io, use_container_width=True)
                    except Exception as e:
                        st.error(f"Erro ao exibir imagem")
                
                # Verificar campo aninhado antigo para compatibilidade (posts antigos)
                elif "imagem" in post and isinstance(post["imagem"], dict) and "base64" in post["imagem"]:
                    try:
                        img_base64 = post["imagem"]["base64"]
                        img_bytes = base64.b64decode(img_base64)
                        img_io = io.BytesIO(img_bytes)
                        st.image(img_io, use_container_width=True)
                    except Exception as e:
                        st.error(f"Erro ao exibir imagem")
        
        # Botão de like na coluna lateral
        with col_like:
            # Sistema de like personalizado
            like_text = "❤️" if usuario_deu_like else "🤍"
            like_count = post.get("likes", 0)
            
            if st.button(f"{like_text} {like_count}", key=f"like_{post_id}", 
                        help="Clique para curtir/descurtir este post"):
                alternar_like(post_id)
                st.rerun()
        
        # Adicionar espaço entre os posts
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
