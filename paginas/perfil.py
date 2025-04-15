import streamlit as st
from paginas.funcoes import obter_perfil_usuario, atualizar_perfil_usuario, registrar_acao_usuario

# Removido: st.set_page_config(layout="centered") 

st.title("Meu Perfil")

# Estilo personalizado simplificado
st.markdown("""
<style>
    .info-label {
        font-weight: bold;
        color: #555;
        margin-bottom: 2px;
    }
    .info-value {
        background-color: #f8f9fa;
        padding: 8px 12px;
        border-radius: 5px;
        margin-bottom: 10px;
        font-size: 1.05em;
    }
    .profile-container {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 8px;
        background-color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# Obter dados atuais do perfil
perfil = obter_perfil_usuario()
if perfil:
    # Estilo CSS personalizado para o perfil
    st.markdown("""
        <style>
        .profile-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .profile-header {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
        }
        .profile-avatar {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid #fff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .profile-name {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50; /* Cor mais escura para o nome */
            margin-left: 20px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* Colunas responsivas */
            gap: 20px;
            margin-top: 20px;
        }
        .info-item {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .info-label {
            color: #7f8c8d; /* Cinza suave para o label */
            font-size: 14px;
            margin-bottom: 5px;
        }
        .info-value {
            color: #2c3e50; /* Mesma cor do nome */
            font-size: 16px;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

    # Container principal do perfil
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    
    # Cabeçalho do perfil com foto e nome
    st.markdown('<div class="profile-header">', unsafe_allow_html=True)
    
    # Foto do perfil
    foto_url = perfil.get("foto", "")
    if foto_url:
        st.markdown(f'<img src="{foto_url}" class="profile-avatar">', unsafe_allow_html=True)
    else:
        # Placeholder de avatar mais estilizado
        st.markdown('<div class="profile-avatar" style="background: #e0e0e0; display: flex; align-items: center; justify-content: center; font-size: 40px;">👤</div>', unsafe_allow_html=True)
    
    # Nome do usuário
    st.markdown(f'<div class="profile-name">{perfil.get("nome_completo", "Não informado")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Fecha profile-header
    
    # Grid de informações
    st.markdown('<div class="info-grid">', unsafe_allow_html=True)
    
    # Email
    st.markdown(f'''
        <div class="info-item">
            <div class="info-label">Email</div>
            <div class="info-value">{perfil.get("email", "Não informado")}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Matrícula
    st.markdown(f'''
        <div class="info-item">
            <div class="info-label">Matrícula</div>
            <div class="info-value">{perfil.get("matricula", "Não informado")}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Curso
    st.markdown(f'''
        <div class="info-item">
            <div class="info-label">Curso</div>
            <div class="info-value">{perfil.get("curso", "Não informado")}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # Fecha info-grid
    st.markdown('</div>', unsafe_allow_html=True) # Fecha profile-card

else:
    st.error("Não foi possível carregar as informações do perfil.")




