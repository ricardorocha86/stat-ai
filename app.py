import streamlit as st 
from paginas.funcoes import inicializar_firebase, obter_perfil_usuario, atualizar_perfil_usuario, login_usuario, registrar_acao_usuario
import os

st.set_page_config(
    page_title="Portal de Estatística",  # Novo Título
    page_icon="arquivos/avatar_assistente.jpg", # Alterado para usar o avatar do assistente
    layout='wide',                       # Melhor aproveitamento do espaço
    initial_sidebar_state="expanded"
)

# Inicializa o Firebase
inicializar_firebase() 


# Modo prova: defina como True para desativar aulas, corretor AI, professor AI e avaliação AI
MODO_PROVA = False 

if MODO_PROVA:
    st.sidebar.badge("MODO PROVA ATIVADO", icon=":material/warning:", color = 'blue')
    st.sidebar.caption("Isso significa que a maioria das funcionalidades estão desativadas temporariamente.")


# Estilo CSS personalizado
st.markdown("""
<style>
    .login-container {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        max-width: 500px;
        margin: auto;
    }
    .welcome-text {
        color: #1f1f1f;
        text-align: center;
    }
    .subtitle-text {
        color: #666;
        font-size: 1.1em;
        margin-bottom: 20px;
    }
    .terms-text {
        font-size: 0.75em;
        color: #888;
        margin-top: 15px;
        text-align: center;
        line-height: 1.4;
    }
    .terms-link {
        color: #3399FF; /* Cor azul para o link */
        text-decoration: none;
        cursor: pointer;
    }
    .terms-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)


# Verificação de login
if not hasattr(st.experimental_user, 'is_logged_in') or not st.experimental_user.is_logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo centralizada
        st.image('arquivos/capa.jpg', width=200, use_container_width=True)
        st.markdown('<h1 class="welcome-text">Bem-vindo ao Portal de Estatística!</h1>', unsafe_allow_html=True) # Novo Texto
        st.markdown('<p class="subtitle-text" style="text-align: center;">Faça login com sua conta Google para acessar o material.</p>', unsafe_allow_html=True) # Novo Texto
        # Botão de login
        if st.button("Login com Google", type="primary", use_container_width=True, icon=':material/login:'):
            # Registra o usuário no Firestore se for o primeiro acesso (login_usuario faz isso)
            # REMOVIDO DAQUI: login_usuario() 
            st.login() # Função de login do Streamlit (redireciona)
        
        # Carrega conteúdo dos Termos para o Popover
        termos_content = "Não foi possível carregar os Termos de Uso e Política de Privacidade."
        try:
            termos_path = os.path.join(os.path.dirname(__file__), 'termos_e_privacidade.md')
            with open(termos_path, 'r', encoding='utf-8') as file:
                termos_content = file.read()
        except Exception as e:
            print(f"Erro ao carregar termos em app.py: {e}") # Log do erro
            # Mantém a mensagem padrão de erro
            
        # Popover com os termos carregados
        with st.popover("Ao fazer login, você concorda com nossos Termos de Uso e Política de Privacidade", use_container_width=True):
            st.markdown(termos_content, unsafe_allow_html=True)
            
 
else:
    # Logo
    st.logo('arquivos/logo.jpg')

    # Garante que o usuário está registrado/atualizado no Firestore ANTES de obter o perfil
    login_usuario() # ADICIONADO AQUI

    # Verifica o perfil para o flag de primeiro acesso
    perfil = obter_perfil_usuario()

    if perfil and not perfil.get("primeiro_acesso_concluido", False):
        # --- Formulário de Primeiro Acesso ---
        st.title("📝 Complete seu Cadastro")
        st.info("Precisamos de algumas informações adicionais para personalizar sua experiência.")
        
        with st.form(key="primeiro_acesso_form", clear_on_submit=False):
            nome_completo = st.text_input("Nome Completo:", key="form_nome")
            matricula = st.text_input("Número de Matrícula:", key="form_matricula")
            curso = st.pills("Seu Curso:", ["Farmácia (MATA44)", "Nutrição (MAT027)"], key="form_curso")
            
            # Checkbox de consentimento
            st.markdown("### 🚀 Antes de começar!")
            st.markdown("Alunos, quero que vocês explorem à vontade e testem tudo o que puderem! Cada clique, sugestão ou ideia de vocês me ajuda a tornar a plataforma ainda melhor para todos. Conto com vocês!")
            consentimento = st.checkbox("Eu entendo que todos os recursos de IA desta plataforma são experimentais, para testes educacionais e em desenvolvimento. Usarei com cautela e reportarei qualquer coisa estranha que encontrar!")
            
            # Botão sempre ativo
            submitted = st.form_submit_button("Salvar Informações", type="primary")
            
            if submitted:
                if not consentimento:
                    st.error("Ops! Você precisa marcar a caixa de consentimento para continuar. Entendemos que está ansioso para começar, mas é importante que você esteja ciente sobre o uso dos recursos de IA.")
                elif not nome_completo or not matricula or not curso:
                    st.warning("Por favor, preencha todos os campos.")
                else:
                    dados_atualizar = {
                        "nome_completo": nome_completo,
                        "matricula": matricula,
                        "curso": curso,
                        "primeiro_acesso_concluido": True,
                        "consentimento_ia": True
                    }
                    if atualizar_perfil_usuario(dados_atualizar):
                        st.success("Cadastro concluído! Você será redirecionado.")
                        st.balloons()
                        st.rerun() # Força o recarregamento da página para sair do form
                    else:
                        st.error("Houve um erro ao salvar seus dados. Tente novamente.")
    
    elif perfil: # Primeiro acesso concluído ou perfil carregado corretamente
        # --- Navegação Principal do App ---
        
        # Define a estrutura das páginas
        if MODO_PROVA:
            paginas = {
                "Área do Aluno": [
                    #st.Page("paginas/inicial.py", title="Início", icon='🏠', default=True), 
                    #st.Page("paginas/aulas.py", title="Aulas", icon='📚'), 
                    #st.Page("paginas/exercicios.py", title="Corretor AI", icon='✍️'),
                    #st.Page("paginas/chatbot.py", title="Professor AI", icon='👨🏽‍🏫'),
                    #st.Page("paginas/prova.py", title="Avaliação AI", icon='📝'),
                    #st.Page("paginas/forum.py", title="Fórum", icon='💬'),
                    #st.Page("paginas/listas.py", title="Listas de Exercícios", icon='📚'),
                    st.Page("paginas/calculadora_normal.py", title="Calculadora da Normal", icon='🧮', default=True),
                    #st.Page("paginas/guided_learning.py", title="Guided Learning Experience", icon='🔮'),
                ],
                "Minha Conta": [ 
                    st.Page("paginas/perfil.py", title="Meu Perfil", icon='👤'), 
                    st.Page("paginas/termos.py", title="Termos e Privacidade", icon='📜'), 
                ],
                "Admin": [ 
                    st.Page("paginas/admin.py", title="Painel Admin", icon='⚙️')
                ] 
            }

        # Adiciona páginas se não estiver em modo prova
        if not MODO_PROVA:
            paginas = {
                "Área do Aluno": [
                    st.Page("paginas/inicial.py", title="Início", icon='🏠', default=True), 
                    st.Page("paginas/aulas.py", title="Aulas", icon='📚'), 
                    st.Page("paginas/exercicios.py", title="Corretor AI", icon='✍️'),
                    st.Page("paginas/chatbot.py", title="Professor AI", icon='👨🏽‍🏫'),
                    st.Page("paginas/prova.py", title="Avaliação AI", icon='📝'),
                    #st.Page("paginas/forum.py", title="Fórum", icon='💬'),
                    st.Page("paginas/listas.py", title="Listas de Exercícios", icon='📚'),
                    st.Page("paginas/calculadora_normal.py", title="Calculadora da Normal", icon='🧮'),
                    #st.Page("paginas/guided_learning.py", title="Guided Learning Experience", icon='🔮'),
                ],
                "Minha Conta": [ 
                    st.Page("paginas/perfil.py", title="Meu Perfil", icon='👤'), 
                    st.Page("paginas/termos.py", title="Termos e Privacidade", icon='📜'), 
                ],
                "Admin": [ 
                    st.Page("paginas/admin.py", title="Painel Admin", icon='⚙️')
                ] 
            }

        # --- DEBUGGING ADMIN CHECK REMOVIDO ---
        # st.sidebar.write("--- DEBUG INFO ---")
        usuario_email = getattr(st.experimental_user, 'email', None)
        # st.sidebar.write(f"Email Logado: {usuario_email}")
        is_admin = False # Default para não admin
        try:
            admin_emails = st.secrets.get("admin_config", {}).get("admin_emails", [])
            # st.sidebar.write(f"Admin Emails (Secrets): {admin_emails}")
            if usuario_email and admin_emails: # Verifica se ambos existem
                is_admin = usuario_email in admin_emails
            # st.sidebar.write(f"É Admin? {is_admin}")
        except Exception as e:
            # st.sidebar.write(f"Erro ao ler secrets/verificar admin: {e}")
            pass # Continua silenciosamente se houver erro ao verificar admin
        # st.sidebar.write("--------------------")
        # --- FIM DEBUGGING ---

        # Remove a seção Admin se o usuário NÃO for admin
        if not is_admin:
            if "Admin" in paginas:
                del paginas["Admin"]
                # st.sidebar.write("(Debug: Seção Admin REMOVIDA)") 
        # else:
             # st.sidebar.write("(Debug: Seção Admin MANTIDA)") 

        # Usa a estrutura de páginas final (com ou sem Admin)
        pg = st.navigation(paginas)
        pg.run()

        # --- Botão de Logout Global na Sidebar ---
        with st.sidebar:
            st.divider() # Adiciona um divisor antes do botão
            if st.button("Logout",
                         key="logout_button_global", # Chave diferente para evitar conflito
                         type='secondary',
                         icon=':material/logout:',
                         use_container_width=True):
                registrar_acao_usuario("Logout", "Usuário fez logout do sistema (botão global)")
                st.logout()
            # st.write(" ") # Adiciona espaço se necessário visualmente

    else: # Caso o perfil não possa ser carregado após o login
        st.error("Não foi possível carregar as informações do seu perfil. Tente recarregar a página ou contate o suporte.")

