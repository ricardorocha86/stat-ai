import streamlit as st
from paginas.funcoes import obter_perfil_usuario, registrar_acao_usuario
import datetime

# CSS personalizado
st.markdown("""
<style>
.welcome-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.quick-access-btn {
    background: white;
    border: 1px solid #e0e0e0;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.quick-access-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.quick-access-btn h3 {
    margin-bottom: 1rem;
    color: #1f1f1f;
    font-size: 1.3rem;
}

.quick-access-btn p {
    color: #666;
    font-size: 0.95rem;
    margin: 0;
    line-height: 1.5;
}

.quick-access-btn ul {
    text-align: left;
    color: #666;
    font-size: 0.9rem;
    padding-left: 1.2rem;
    margin-top: 0.8rem;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 2.5rem 0 1.5rem 0;
    color: #1f1f1f;
    padding-left: 0.5rem;
    border-left: 4px solid #667eea;
}

.footer-note {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #ff9800;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Obtém dados do perfil
perfil = obter_perfil_usuario()
nome_usuario = perfil.get("nome_completo", "").split()[0] if perfil.get("nome_completo") else "Aluno(a)"
curso = perfil.get("curso", "")

# Header de boas-vindas
st.markdown(f"""
<div class="welcome-header">
    <h1>👋 Olá, {nome_usuario}!</h1>
    <p>Bem-vindo(a) ao seu Portal de Estatística - {curso}</p>
</div>
""", unsafe_allow_html=True)

# --- Seção de Últimas Atualizações ---
st.markdown("""
<div style="background-color: #eef2f7; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; border-left: 5px solid #4CAF50;">
    <h3 style="color: #2c3e50; margin-top: 0;">🚀 Últimas Atualizações no Portal!</h3>
    <ul style="list-style-type: disc; margin-left: 20px; color: #34495e;">
        <li><strong>Aulas de Inferência Estatística:</strong> A nova sessão de aulas de Inferência Estatística já está no ar! </li>
        <li><strong>Calculadora da Normal:</strong> Agora temos uma página exclusiva para a Calculadora da Distribuição Normal! Com ela, você pode calcular probabilidades e intervalos de confiança de forma prática e rápida.</li>
        <li><strong>Página de Recursos agora é Listas de Exercícios:</strong> Acesse as Listas de Exercícios 1 a 5 na nova página de Listas de Exercícios.</li>
     </ul>
    <p style="font-size: 0.9em; color: #555; margin-top: 1rem;">Continuamos trabalhando para melhorar sua experiência. Bom estudo!</p>
</div>
""", unsafe_allow_html=True)

# Acesso Rápido
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="quick-access-btn">
        <h3>📚 Aulas</h3>
        <p>Acesse todo o conteúdo do curso de forma digital, além de recursos de IA como quizzes interativos para testar seu conhecimento.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar Aulas", key="btn_aulas", use_container_width=True):
        registrar_acao_usuario("Navegação", "Acesso à página de Aulas pela pagina principal")
        st.switch_page("paginas/aulas.py")

with col2:
    st.markdown("""
    <div class="quick-access-btn">
        <h3>🤖 Professor AI</h3>
        <p>Tire suas dúvidas a qualquer momento com nosso assistente inteligente que oferece explicações personalizadas.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Falar com IA", key="btn_ia", use_container_width=True):
        registrar_acao_usuario("Navegação", "Acesso ao Professor AI pela pagina principal")
        st.switch_page("paginas/chatbot.py")

with col3:
    st.markdown("""
    <div class="quick-access-btn">
        <h3>💬 Fórum</h3>
        <p>Participe das discussões com seus colegas, compartilhe conhecimento e tire dúvidas em comunidade.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar Fórum", key="btn_forum", use_container_width=True):
        registrar_acao_usuario("Navegação", "Acesso ao Fórum pela pagina principal")
        st.switch_page("paginas/forum.py")

# Ferramentas de Estudo 
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="quick-access-btn">
        <h3>✍️ Exercícios</h3>
        <p>Pratique com exercícios específicos para cada tema, com correção automática e feedback detalhado.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ver Exercícios", key="btn_exercicios", use_container_width=True):
        registrar_acao_usuario("Navegação", "Acesso aos Exercícios pela pagina principal")
        st.switch_page("paginas/exercicios.py")

with col2:
    st.markdown("""
    <div class="quick-access-btn">
        <h3>📊 Avaliações</h3>
        <p>Teste seu conhecimento com simulados e questões adaptativas que ajudam a medir seu progresso. Tudo gerado com base no material de aula.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Fazer Avaliação", key="btn_avaliacoes", use_container_width=True):
        registrar_acao_usuario("Navegação", "Acesso às Avaliações pela pagina principal")
        st.switch_page("paginas/prova.py")

with col3:
    st.markdown("""
    <div class="quick-access-btn">
        <h3>📑 Recursos</h3>
        <p>Acesse materiais complementares como a Tabela TACO, resumos e outros recursos de apoio ao estudo.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ver Recursos", key="btn_recursos", use_container_width=True):
        registrar_acao_usuario("Navegação", "Acesso aos Recursos pela pagina principal")
        st.switch_page("paginas/recursos.py")

# Rodapé com informações de uso da IA
st.markdown("""
<div class="footer-note">
    <p style="font-size: 0.9rem; color: #666; margin: 0;">
        <strong>⚠️ Uso Consciente da IA:</strong> A inteligência artificial é uma ferramenta de apoio aos seus estudos.
        Mantenha sempre seu pensamento crítico e, em caso de dúvidas complexas, consulte seu professor.
    </p>
</div>
""", unsafe_allow_html=True)