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

senha = st.text_input('Senha de administrador:', type='password')
if senha == 'eita':
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
        usuarios_emails = df_usuarios['Email'].tolist()
        usuario_selecionado = st.selectbox("Selecione um usuário para ver detalhes:", usuarios_emails)
        
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
                    df_acoes['Data'] = pd.to_datetime(df_acoes['Data/Hora'], dayfirst=True).dt.date
                    acoes_por_dia = df_acoes['Data'].value_counts().sort_index()
                    fig = px.line(x=acoes_por_dia.index, y=acoes_por_dia.values, 
                                title='Ações por Dia',
                                labels={'x': 'Data', 'y': 'Quantidade de Ações'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Nenhuma ação registrada para este usuário")
            
            with tab_atividades:
                dados_atividades = []
                for atividade in atividades:
                    atividade_data = atividade.to_dict()
                    data_hora = atividade_data.get('data_hora', None)
                    dados_atividades.append({
                        "Tipo": atividade_data.get('tipo', 'Desconhecido'),
                        "Módulo": atividade_data.get('modulo', 'Desconhecido'),
                        "Data/Hora": data_hora.strftime('%d/%m/%Y %H:%M:%S') if data_hora else '',
                        "Detalhes": str(atividade_data.get('detalhes', ''))
                    })
                
                if dados_atividades:
                    df_atividades = pd.DataFrame(dados_atividades)
                    
                    # Métricas de atividades
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Módulos Diferentes", len(df_atividades['Módulo'].unique()))
                    with col2:
                        st.metric("Tipos de Atividade", len(df_atividades['Tipo'].unique()))
                    
                    # Tabela de atividades
                    st.subheader("Todas as Atividades")
                    st.dataframe(df_atividades.sort_values(by="Data/Hora", ascending=False),
                               hide_index=True, use_container_width=True)
                    
                    # Gráficos
                    col1, col2 = st.columns(2)
                    with col1:
                        # Gráfico de atividades por módulo
                        atividades_modulo = df_atividades['Módulo'].value_counts()
                        fig = px.bar(x=atividades_modulo.index, y=atividades_modulo.values,
                                   title="Atividades por Módulo",
                                   labels={'x': 'Módulo', 'y': 'Quantidade'})
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Gráfico de tipos de atividade
                        atividades_tipo = df_atividades['Tipo'].value_counts()
                        fig = px.pie(values=atividades_tipo.values, names=atividades_tipo.index,
                                   title="Distribuição por Tipo de Atividade")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Nenhuma atividade acadêmica registrada para este usuário")
            
            with tab_chats:
                dados_chats = []
                for chat in chats:
                    chat_data = chat.to_dict()
                    mensagens = chat_data.get('mensagens', [])
                    data_criacao = chat_data.get('data_criacao', '')
                    ultima_atualizacao = chat_data.get('ultima_atualizacao', '')
                    
                    dados_chats.append({
                        "Nome": chat_data.get('nome', 'Chat sem nome'),
                        "Mensagens": len(mensagens),
                        "Data Criação": data_criacao.strftime('%d/%m/%Y %H:%M:%S') if data_criacao else '',
                        "Última Atualização": ultima_atualizacao.strftime('%d/%m/%Y %H:%M:%S') if ultima_atualizacao else '',
                        "ID": chat.id
                    })
                
                if dados_chats:
                    df_chats = pd.DataFrame(dados_chats)
                    st.dataframe(df_chats.sort_values(by="Última Atualização", ascending=False),
                               hide_index=True, use_container_width=True)
                    
                    # Visualização de chat específico
                    chat_ids = df_chats['ID'].tolist()
                    if chat_ids:
                        chat_selecionado = st.selectbox("Selecione um chat para ver as mensagens:", chat_ids)
                        if chat_selecionado:
                            chat_doc = db.collection(COLECAO_USUARIOS).document(usuario_selecionado).collection("chats").document(chat_selecionado).get()
                            if chat_doc.exists:
                                chat_data = chat_doc.to_dict()
                                mensagens = chat_data.get('mensagens', [])
                                
                                st.subheader(f"Mensagens do chat: {chat_data.get('nome', 'Chat sem nome')}")
                                
                                for i, msg in enumerate(mensagens):
                                    role = msg.get('role', '')
                                    content = msg.get('content', '')
                                    
                                    if role == "user":
                                        st.markdown(f"**Usuário**: {content}")
                                    elif role == "assistant":
                                        st.markdown(f"**Assistente**: {content}")
                                    
                                    if i < len(mensagens) - 1:
                                        st.divider()
                else:
                    st.info("Nenhum chat encontrado para este usuário")
    
    with tab3:
        st.header("Dados Detalhados")
        
        # Opções para visualização
        visualizacao = st.selectbox("O que deseja visualizar?", 
                                   ["Linha do Tempo do Usuário", "Todos os Logs", "Usuários por Período", "Exportar Dados"])
        
        if visualizacao == "Linha do Tempo do Usuário":
            # Seleção do usuário
            usuario_timeline = st.selectbox(
                "Selecione um usuário para ver sua linha do tempo:",
                [u["Email"] for u in dados_usuarios],
                key="usuario_timeline"
            )
            
            if usuario_timeline:
                # Coletar todas as interações do usuário
                timeline_data = []
                
                # Coletar logs
                logs = db.collection(COLECAO_USUARIOS).document(usuario_timeline).collection("logs").get()
                for log in logs:
                    log_data = log.to_dict()
                    data_hora = log_data.get('data_hora', None)
                    if data_hora:
                        timeline_data.append({
                            "Data_Hora": data_hora,
                            "Tipo": "Log",
                            "Ação": log_data.get('acao', 'Desconhecida'),
                            "Detalhes": str(log_data.get('detalhes', '')),
                            "Data_Hora_Formatada": data_hora.strftime('%d/%m/%Y %H:%M:%S')
                        })
                
                # Coletar atividades acadêmicas
                atividades = db.collection(COLECAO_USUARIOS).document(usuario_timeline).collection("atividades_academicas").get()
                for atividade in atividades:
                    atividade_data = atividade.to_dict()
                    data_hora = atividade_data.get('data_hora', None)
                    if data_hora:
                        timeline_data.append({
                            "Data_Hora": data_hora,
                            "Tipo": "Atividade Acadêmica",
                            "Ação": f"{atividade_data.get('tipo', 'Desconhecida')} - {atividade_data.get('modulo', 'Módulo Desconhecido')}",
                            "Detalhes": str(atividade_data.get('detalhes', '')),
                            "Data_Hora_Formatada": data_hora.strftime('%d/%m/%Y %H:%M:%S')
                        })
                
                # Coletar chats
                chats = db.collection(COLECAO_USUARIOS).document(usuario_timeline).collection("chats").get()
                for chat in chats:
                    chat_data = chat.to_dict()
                    data_criacao = chat_data.get('data_criacao', None)
                    if data_criacao:
                        timeline_data.append({
                            "Data_Hora": data_criacao,
                            "Tipo": "Chat",
                            "Ação": f"Novo chat criado: {chat_data.get('nome', 'Chat sem nome')}",
                            "Detalhes": f"Total de mensagens: {len(chat_data.get('mensagens', []))}",
                            "Data_Hora_Formatada": data_criacao.strftime('%d/%m/%Y %H:%M:%S')
                        })
                
                if timeline_data:
                    # Criar DataFrame e ordenar por data/hora
                    df_timeline = pd.DataFrame(timeline_data)
                    df_timeline = df_timeline.sort_values('Data_Hora_Formatada', ascending=False)
                    
                    # Exibir métricas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Interações", len(df_timeline))
                    with col2:
                        st.metric("Tipos de Ação", len(df_timeline['Ação'].unique()))
                    with col3:
                        dias_ativo = len(df_timeline['Data_Hora'].dt.date.unique())
                        st.metric("Dias de Atividade", dias_ativo)
                    
                    # Exibir linha do tempo
                    st.subheader("Linha do Tempo Completa")
                    st.dataframe(
                        df_timeline[['Data_Hora_Formatada', 'Tipo', 'Ação', 'Detalhes']].rename(
                            columns={'Data_Hora_Formatada': 'Data/Hora'}
                        ),
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # Gráfico de atividade ao longo do tempo
                    st.subheader("Distribuição de Atividades")
                    atividades_por_tipo = df_timeline['Tipo'].value_counts()
                    fig = px.pie(values=atividades_por_tipo.values, 
                               names=atividades_por_tipo.index,
                               title="Distribuição por Tipo de Atividade")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Gráfico de atividade por dia
                    df_timeline['Data'] = df_timeline['Data_Hora'].dt.date
                    atividades_por_dia = df_timeline['Data'].value_counts().sort_index()
                    fig = px.line(x=atividades_por_dia.index, 
                                y=atividades_por_dia.values,
                                title="Atividades por Dia",
                                labels={'x': 'Data', 'y': 'Quantidade de Atividades'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Nenhuma atividade encontrada para este usuário.")
        
        elif visualizacao == "Todos os Logs":
            # Período para análise
            periodo = st.selectbox("Período de análise:", 
                                 ["Últimos 7 dias", "Últimos 30 dias", "Todo o período"])
            
            # Definir data de corte com base no período selecionado, usando UTC
            data_corte = hoje
            if periodo == "Últimos 7 dias":
                data_corte = hoje - timedelta(days=7)
            elif periodo == "Últimos 30 dias":
                data_corte = hoje - timedelta(days=30)
            
            # Coletar todos os logs no período selecionado
            todos_logs = []
            for usuario in dados_usuarios:
                email = usuario["Email"]
                logs = db.collection(COLECAO_USUARIOS).document(email).collection("logs").get()
                
                for log in logs:
                    log_data = log.to_dict()
                    data_hora = log_data.get('data_hora', None)
                    
                    if data_hora and (periodo == "Todo o período" or data_hora >= data_corte):
                        todos_logs.append({
                            "Usuario": email,
                            "Acao": log_data.get('acao', 'Desconhecida'),
                            "Data_Hora": data_hora,  # Objeto datetime completo para ordenação
                            "Data": data_hora.strftime('%d/%m/%Y'),
                            "Hora": data_hora.strftime('%H:00'),
                            "Detalhes": str(log_data.get('detalhes', ''))
                        })
            
            # Criar DataFrame com todos os logs
            df_todos_logs = pd.DataFrame(todos_logs)
            
            if not df_todos_logs.empty:
                # Ordenar o DataFrame principal por Data_Hora para uso consistente
                df_todos_logs = df_todos_logs.sort_values(by="Data_Hora", ascending=False)
                
                # Exibir tabela com logs filtrados
                st.subheader("Logs Detalhados")
                df_logs_display = df_todos_logs[['Usuario', 'Acao', 'Data', 'Hora', 'Detalhes']]
                st.dataframe(df_logs_display, hide_index=True, use_container_width=True)
                
                # Busca por palavra-chave
                st.subheader("Busca por Palavra-chave nos Logs")
                palavra_chave = st.text_input("Digite a palavra-chave para buscar:")
                if palavra_chave:
                    filtro_palavra = df_logs_display[
                        df_logs_display['Acao'].str.contains(palavra_chave, case=False) | 
                        df_logs_display['Detalhes'].str.contains(palavra_chave, case=False)
                    ]
                    
                    if not filtro_palavra.empty:
                        st.write(f"Foram encontrados {len(filtro_palavra)} resultados para '{palavra_chave}':")
                        st.dataframe(filtro_palavra, hide_index=True, use_container_width=True)
                    else:
                        st.info(f"Nenhum resultado encontrado para '{palavra_chave}'.")
            else:
                st.info(f"Não há dados de logs para o período selecionado ({periodo}).")
                
        elif visualizacao == "Usuários por Período":
            # Agrupar usuários por data de cadastro
            df_usuarios['Data Cadastro Curta'] = df_usuarios['Data Cadastro'].str.split(' ').str[0]
            usuarios_por_dia = df_usuarios['Data Cadastro Curta'].value_counts().reset_index()
            usuarios_por_dia.columns = ['Data', 'Novos Usuários']
            usuarios_por_dia = usuarios_por_dia.sort_values('Data')
            
            fig = px.bar(usuarios_por_dia, x='Data', y='Novos Usuários',
                       title='Novos Usuários por Dia')
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela completa
            st.subheader("Detalhamento de Usuários por Data de Cadastro")
            st.dataframe(
                df_usuarios[['Nome', 'Email', 'Data Cadastro', 'Último Acesso']],
                hide_index=True,
                use_container_width=True
            )
            
        elif visualizacao == "Exportar Dados":
            # Opção para exportar dados
            st.subheader("Exportar Dados")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Exportar Lista de Usuários (CSV)", use_container_width=True):
                    csv = df_usuarios.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{COLECAO_USUARIOS}_{datetime.now(timezone.utc).strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                    )
            with col2:
                if st.button("Exportar Todos os Logs (CSV)", use_container_width=True):
                    # Criar DataFrame com todos os logs para exportação
                    todos_logs_export = []
                    for usuario in dados_usuarios:
                        email = usuario["Email"]
                        logs = db.collection(COLECAO_USUARIOS).document(email).collection("logs").get()
                        
                        for log in logs:
                            log_data = log.to_dict()
                            data_hora = log_data.get('data_hora', '')
                            todos_logs_export.append({
                                "Usuario": email,
                                "Acao": log_data.get('acao', ''),
                                "Data_Hora": data_hora.strftime('%d/%m/%Y %H:%M:%S') if data_hora else '',
                                "Detalhes": str(log_data.get('detalhes', ''))
                            })
                    
                    df_logs_export = pd.DataFrame(todos_logs_export)
                    csv = df_logs_export.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"logs_{datetime.now(timezone.utc).strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                    )

else:
    st.warning("Por favor, digite a senha correta para acessar o painel administrativo.")

st.divider()
st.page_link("paginas/chatbot.py", label=" Voltar para as conversas", icon="🏃", )
