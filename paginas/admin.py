import streamlit as st 

from datetime import datetime, timedelta, timezone
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from firebase_admin import firestore
from paginas.funcoes import registrar_acao_usuario, COLECAO_USUARIOS

st.title("🔐 Painel Administrativo")

st.write("Aplicativo desenvolvido por [@ricardorocha86](https://www.linkedin.com/in/ricardorocha86/)")
st.write('Versão 0.0.3')

# Inicializar o cliente Firestore
db = firestore.client()

# Criar guias para organizar o dashboard
tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "👥 Usuários", "🔍 Dados Detalhados"])

with tab1:
    st.header("Visão Geral do Sistema")
    
    # Obter dados gerais para o dashboard
    usuarios = db.collection(COLECAO_USUARIOS).get()
    dados_usuarios = []
    total_acoes = 0
    total_atividades_academicas = 0
    usuarios_ativos_7dias = 0
    hoje = datetime.now(timezone.utc)
    data_7dias_atras = hoje - timedelta(days=7)
    
    # Dados para gráficos
    acoes_por_dia = {}
    acoes_por_tipo = {}
    atividades_por_modulo = {}
    atividades_por_tipo = {}
    
    for usuario in usuarios:
        dados = usuario.to_dict()
        email = dados.get("email", "")
        ultimo_acesso = dados.get("ultimo_acesso", None)
        
        # Contar usuários ativos nos últimos 7 dias
        if ultimo_acesso and ultimo_acesso > data_7dias_atras:
            usuarios_ativos_7dias += 1
        
        # Obter logs do usuário
        logs = db.collection(COLECAO_USUARIOS).document(email).collection("logs").get()
        acoes_usuario = len(logs)
        total_acoes += acoes_usuario
        
        # Obter atividades acadêmicas do usuário
        atividades = db.collection(COLECAO_USUARIOS).document(email).collection("atividades_academicas").get()
        atividades_usuario = len(atividades)
        total_atividades_academicas += atividades_usuario
        
        # Processar logs para estatísticas
        for log in logs:
            log_data = log.to_dict()
            data_hora = log_data.get('data_hora', None)
            tipo_acao = log_data.get('acao', 'Desconhecida')
            
            if data_hora:
                data_str = data_hora.strftime('%d/%m/%Y')
                acoes_por_dia[data_str] = acoes_por_dia.get(data_str, 0) + 1
            
            acoes_por_tipo[tipo_acao] = acoes_por_tipo.get(tipo_acao, 0) + 1
        
        # Processar atividades acadêmicas para estatísticas
        for atividade in atividades:
            atividade_data = atividade.to_dict()
            modulo = atividade_data.get('modulo', 'Desconhecido')
            tipo = atividade_data.get('tipo', 'Desconhecido')
            
            atividades_por_modulo[modulo] = atividades_por_modulo.get(modulo, 0) + 1
            atividades_por_tipo[tipo] = atividades_por_tipo.get(tipo, 0) + 1
        
        # Adicionar usuário à lista
        dados_usuarios.append({
            "Nome": dados.get("nome", ""),
            "Email": email,
            "Primeiro Nome": dados.get("primeiro_nome", ""),
            "Data Cadastro": dados.get("data_cadastro", "").strftime("%d/%m/%Y %H:%M:%S") if dados.get("data_cadastro") else "",
            "Último Acesso": dados.get("ultimo_acesso", "").strftime("%d/%m/%Y %H:%M:%S") if dados.get("ultimo_acesso") else "",
            "Ações Totais": acoes_usuario,
            "Atividades Acadêmicas": atividades_usuario,
        })
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Usuários", len(dados_usuarios))
    with col2:
        st.metric("Usuários Ativos (7 dias)", usuarios_ativos_7dias)
    with col3:
        st.metric("Total de Ações", total_acoes)
    with col4:
        st.metric("Total de Atividades Acadêmicas", total_atividades_academicas)
    
    # Gráficos para a visão geral
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Atividade por Dia")
        if acoes_por_dia:
            df_dias = pd.DataFrame({
                'Data': list(acoes_por_dia.keys()),
                'Ações': list(acoes_por_dia.values())
            })
            df_dias = df_dias.sort_values('Data')
            fig = px.bar(df_dias, x='Data', y='Ações', title='Ações por Dia')
            fig.update_layout(xaxis_title='Data', yaxis_title='Número de Ações')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Não há dados suficientes para gerar o gráfico de atividade diária.")
    
    with col2:
        st.subheader("Tipos de Ação")
        if acoes_por_tipo:
            df_tipos = pd.DataFrame({
                'Tipo': list(acoes_por_tipo.keys()),
                'Contagem': list(acoes_por_tipo.values())
            })
            df_tipos = df_tipos.sort_values('Contagem', ascending=False)
            fig = px.pie(df_tipos, values='Contagem', names='Tipo', title='Distribuição de Tipos de Ação')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Não há dados suficientes para gerar o gráfico de tipos de ação.")
            
    # Novos gráficos para atividades acadêmicas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Atividades por Módulo")
        if atividades_por_modulo:
            df_modulos = pd.DataFrame({
                'Módulo': list(atividades_por_modulo.keys()),
                'Contagem': list(atividades_por_modulo.values())
            })
            df_modulos = df_modulos.sort_values('Contagem', ascending=False)
            fig = px.bar(df_modulos, x='Módulo', y='Contagem', title='Atividades por Módulo')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Não há dados suficientes para gerar o gráfico de atividades por módulo.")
    
    with col2:
        st.subheader("Tipos de Atividade Acadêmica")
        if atividades_por_tipo:
            df_tipos_ativ = pd.DataFrame({
                'Tipo': list(atividades_por_tipo.keys()),
                'Contagem': list(atividades_por_tipo.values())
            })
            df_tipos_ativ = df_tipos_ativ.sort_values('Contagem', ascending=False)
            fig = px.pie(df_tipos_ativ, values='Contagem', names='Tipo', title='Distribuição de Tipos de Atividade')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Não há dados suficientes para gerar o gráfico de tipos de atividade.")

with tab2:
    st.header("Gerenciamento de Usuários")
    
    # Criar DataFrame com dados de usuários
    df_usuarios = pd.DataFrame(dados_usuarios)
    
    # Filtros para usuários
    col1, col2 = st.columns(2)
    with col1:
        filtro_nome = st.text_input("Filtrar por Nome:")
    with col2:
        filtro_email = st.text_input("Filtrar por Email:")
    
    # Aplicar filtros
    df_filtrado = df_usuarios.copy()
    if filtro_nome:
        df_filtrado = df_filtrado[df_filtrado['Nome'].str.contains(filtro_nome, case=False)]
    if filtro_email:
        df_filtrado = df_filtrado[df_filtrado['Email'].str.contains(filtro_email, case=False)]
    
    # Exibir tabela de usuários com ordem personalizada
    st.dataframe(
        df_filtrado.sort_values(by="Último Acesso", ascending=False), 
        hide_index=True, 
        use_container_width=True
    )
    
    # Detalhes do usuário
    st.write("### Detalhes do Usuário")
    if not df_usuarios.empty:
        usuarios_emails = df_usuarios['Email'].tolist()
        usuario_selecionado = st.selectbox("Selecione um usuário para ver detalhes:", usuarios_emails, key="admin_select_user_details")
        
        if usuario_selecionado:
            # Criar tabs para diferentes tipos de informação
            tab_metricas, tab_acoes, tab_atividades, tab_chats = st.tabs([
                "📈 Métricas", 
                "🔄 Ações",
                "📚 Atividades Acadêmicas",
                "💬 Chats"
            ])
            
            # Buscar dados do usuário
            logs = db.collection(COLECAO_USUARIOS).document(usuario_selecionado).collection("logs").get()
            atividades = db.collection(COLECAO_USUARIOS).document(usuario_selecionado).collection("atividades_academicas").get()
            chats = db.collection(COLECAO_USUARIOS).document(usuario_selecionado).collection("chats").get()
            
            with tab_metricas:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total de Ações", len(logs))
                with col2:
                    st.metric("Total de Atividades", len(atividades))
                with col3:
                    st.metric("Total de Chats", len(chats))
                with col4:
                    # Calcular dias ativos
                    todas_datas = []
                    for log in logs:
                        data = log.to_dict().get('data_hora', None)
                        if data:
                            todas_datas.append(data.date())
                    for atividade in atividades:
                        data = atividade.to_dict().get('data_hora', None)
                        if data:
                            todas_datas.append(data.date())
                    dias_ativos = len(set(todas_datas))
                    st.metric("Dias Ativos", dias_ativos)
            
            with tab_acoes:
                dados_acoes = []
                for log in logs:
                    log_data = log.to_dict()
                    data_hora = log_data.get('data_hora', '')
                    dados_acoes.append({
                        "Ação": log_data.get('acao', ''),
                        "Data/Hora": data_hora.strftime('%d/%m/%Y %H:%M:%S') if data_hora else '',
                        "Observações": str(log_data.get('detalhes', ''))
                    })
                
                if dados_acoes:
                    df_acoes = pd.DataFrame(dados_acoes)
                    st.dataframe(df_acoes.sort_values(by="Data/Hora", ascending=False),
                               hide_index=True, use_container_width=True)
                    
                    # Gráfico de atividade do usuário
                    st.subheader("Histórico de Atividade")
                    # Certifique-se de que 'Data/Hora' existe e não está vazio antes de converter
                    df_acoes_plot = df_acoes[df_acoes['Data/Hora'] != ''].copy()
                    if not df_acoes_plot.empty:
                        df_acoes_plot['Data'] = pd.to_datetime(df_acoes_plot['Data/Hora'], dayfirst=True).dt.date
                        acoes_por_dia_usuario = df_acoes_plot['Data'].value_counts().sort_index()
                        fig_usuario = px.line(x=acoes_por_dia_usuario.index, y=acoes_por_dia_usuario.values, 
                                            labels={'x': 'Data', 'y': 'Número de Ações'},
                                            title='Atividade do Usuário ao Longo do Tempo')
                        st.plotly_chart(fig_usuario, use_container_width=True)
                    else:
                        st.info("Nenhuma ação com data válida para plotar o gráfico.")                        
                else:
                    st.info("Nenhuma ação registrada para este usuário.")
            
            with tab_atividades:
                dados_atividades = []
                for atividade in atividades:
                    ativ_data = atividade.to_dict()
                    data_hora = ativ_data.get('data_hora', '')
                    dados_atividades.append({
                        "Tipo": ativ_data.get('tipo', ''),
                        "Módulo": ativ_data.get('modulo', ''),
                        "Detalhes": str(ativ_data.get('detalhes', '')),
                        "Data/Hora": data_hora.strftime('%d/%m/%Y %H:%M:%S') if data_hora else ''
                    })
                
                if dados_atividades:
                    df_atividades = pd.DataFrame(dados_atividades)
                    st.dataframe(df_atividades.sort_values(by="Data/Hora", ascending=False),
                                   hide_index=True, use_container_width=True)
                else:
                    st.info("Nenhuma atividade acadêmica registrada para este usuário.")
            
            with tab_chats:
                dados_chats = []
                for chat in chats:
                    chat_data = chat.to_dict()
                    data_criacao = chat_data.get('data_criacao', '') # Campo correto para chats
                    dados_chats.append({
                        "ID do Chat": chat.id,
                        "Título": chat_data.get('titulo_chat', 'Sem título'),
                        "Data Criação": data_criacao.strftime('%d/%m/%Y %H:%M:%S') if data_criacao else '',
                        "Qtd. Mensagens": chat_data.get('numero_mensagens', 0)
                    })
                
                if dados_chats:
                    df_chats = pd.DataFrame(dados_chats)
                    st.dataframe(df_chats.sort_values(by="Data Criação", ascending=False),
                                   hide_index=True, use_container_width=True)
                    
                    chat_id_selecionado = st.selectbox("Selecione um Chat para ver o histórico:", 
                                                       options=[None] + [c.id for c in chats], 
                                                       format_func=lambda x: df_chats[df_chats['ID do Chat'] == x]['Título'].iloc[0] if x else "Nenhum")
                    if chat_id_selecionado:
                        mensagens_ref = db.collection(COLECAO_USUARIOS).document(usuario_selecionado).collection("chats").document(chat_id_selecionado).collection("mensagens").order_by("timestamp").stream()
                        st.markdown("##### Histórico do Chat:")
                        for msg in mensagens_ref:
                            msg_data = msg.to_dict()
                            role = msg_data.get("role")
                            content = msg_data.get("content")
                            avatar_map = {"user": "🧑‍🎓", "assistant": "👨🏽‍🏫"}
                            with st.chat_message(name=role if role else "unknown", avatar=avatar_map.get(role, "❓") ):
                                st.markdown(content)
                else:
                    st.info("Nenhum chat registrado para este usuário.")
    else:
        st.info("Nenhum usuário encontrado ou o DataFrame de usuários está vazio.")

with tab3:
    st.header("Dados Detalhados")
    st.write("Em desenvolvimento...")

    # Funcionalidade de download de dados (exemplo)
    if not df_usuarios.empty:
        csv = df_usuarios.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados de Usuários (CSV)",
            data=csv,
            file_name='dados_usuarios.csv',
            mime='text/csv',
        )
    else:
        st.info("Não há dados de usuários para baixar.")

st.divider()
st.page_link("paginas/chatbot.py", label=" Voltar para as conversas", icon="🏃", )
