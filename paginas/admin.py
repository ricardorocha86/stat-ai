import streamlit as st 
import time
from io import BytesIO

from datetime import datetime, timedelta, timezone
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from firebase_admin import firestore
from paginas.funcoes import registrar_acao_usuario, COLECAO_USUARIOS

SENHA_ADMIN = "eita"

def autenticar_admin():
    if st.session_state.get("admin_senha_input") == SENHA_ADMIN:
        st.session_state["admin_autenticado"] = True
        st.session_state.pop("admin_senha_incorreta", None)
    else:
        st.session_state["admin_senha_incorreta"] = True


if not st.session_state.get("admin_autenticado", False):
    st.title("🔐 Acesso Administrativo")
    st.text_input("Senha", type="password", key="admin_senha_input")
    st.button("Entrar", type="primary", on_click=autenticar_admin)
    if st.session_state.get("admin_senha_incorreta"):
        st.error("Senha incorreta.")
    st.stop()

st.title("🔐 Painel Administrativo")

st.write("Aplicativo desenvolvido por [@ricardorocha86](https://www.linkedin.com/in/ricardorocha86/)")
st.write('Versão 0.0.3')

# Inicializar o cliente Firestore
db = firestore.client()

@st.cache_data(ttl=300, show_spinner=False)
def carregar_usuarios_basicos():
    dados_usuarios = []
    for usuario in db.collection(COLECAO_USUARIOS).get():
        dados = usuario.to_dict() or {}
        dados_usuarios.append({
            "Nome": dados.get("nome_completo") or dados.get("nome_google") or dados.get("nome", ""),
            "Email": dados.get("email", usuario.id),
            "Primeiro Nome": dados.get("primeiro_nome_google") or dados.get("primeiro_nome", ""),
            "Data Cadastro": dados.get("data_cadastro", "").strftime("%d/%m/%Y %H:%M:%S") if dados.get("data_cadastro") else "",
            "Último Acesso": dados.get("ultimo_acesso", "").strftime("%d/%m/%Y %H:%M:%S") if dados.get("ultimo_acesso") else "",
        })
    return dados_usuarios


@st.cache_data(ttl=300, show_spinner=False)
def carregar_visao_geral():
    usuarios = db.collection(COLECAO_USUARIOS).get()
    dados_usuarios = []
    total_acoes = 0
    total_atividades_academicas = 0
    usuarios_ativos_7dias = 0
    data_7dias_atras = datetime.now(timezone.utc) - timedelta(days=7)
    acoes_por_dia = {}
    acoes_por_tipo = {}
    atividades_por_modulo = {}
    atividades_por_tipo = {}

    for usuario in usuarios:
        dados = usuario.to_dict() or {}
        email = dados.get("email", usuario.id)
        ultimo_acesso = dados.get("ultimo_acesso")

        if ultimo_acesso and ultimo_acesso > data_7dias_atras:
            usuarios_ativos_7dias += 1

        logs = db.collection(COLECAO_USUARIOS).document(email).collection("logs").select(["acao", "data_hora"]).get()
        atividades = (
            db.collection(COLECAO_USUARIOS)
            .document(email)
            .collection("atividades_academicas")
            .select(["tipo", "modulo"])
            .get()
        )
        total_acoes += len(logs)
        total_atividades_academicas += len(atividades)

        for log in logs:
            log_data = log.to_dict() or {}
            data_hora = log_data.get("data_hora")
            tipo_acao = log_data.get("acao", "Desconhecida")
            if data_hora:
                data_str = data_hora.strftime("%d/%m/%Y")
                acoes_por_dia[data_str] = acoes_por_dia.get(data_str, 0) + 1
            acoes_por_tipo[tipo_acao] = acoes_por_tipo.get(tipo_acao, 0) + 1

        for atividade in atividades:
            atividade_data = atividade.to_dict() or {}
            modulo = atividade_data.get("modulo", "Desconhecido")
            tipo = atividade_data.get("tipo", "Desconhecido")
            atividades_por_modulo[modulo] = atividades_por_modulo.get(modulo, 0) + 1
            atividades_por_tipo[tipo] = atividades_por_tipo.get(tipo, 0) + 1

        dados_usuarios.append({
            "Nome": dados.get("nome_completo") or dados.get("nome_google") or dados.get("nome", ""),
            "Email": email,
            "Primeiro Nome": dados.get("primeiro_nome_google") or dados.get("primeiro_nome", ""),
            "Data Cadastro": dados.get("data_cadastro", "").strftime("%d/%m/%Y %H:%M:%S") if dados.get("data_cadastro") else "",
            "Último Acesso": ultimo_acesso.strftime("%d/%m/%Y %H:%M:%S") if ultimo_acesso else "",
            "Ações Totais": len(logs),
            "Atividades Acadêmicas": len(atividades),
        })

    return {
        "dados_usuarios": dados_usuarios,
        "total_acoes": total_acoes,
        "total_atividades_academicas": total_atividades_academicas,
        "usuarios_ativos_7dias": usuarios_ativos_7dias,
        "acoes_por_dia": acoes_por_dia,
        "acoes_por_tipo": acoes_por_tipo,
        "atividades_por_modulo": atividades_por_modulo,
        "atividades_por_tipo": atividades_por_tipo,
    }


secao = st.radio(
    "Seção",
    ["📊 Visão Geral", "👥 Usuários", "🔍 Dados Detalhados", "📥 Exportar Dados"],
    horizontal=True,
    label_visibility="collapsed",
)

if secao == "📊 Visão Geral":
    st.header("Visão Geral do Sistema")

    col_carregar, col_atualizar = st.columns([3, 1])
    with col_carregar:
        carregar = st.button("Carregar visão geral", type="primary", use_container_width=True)
    with col_atualizar:
        atualizar = st.button("Atualizar cache", use_container_width=True)

    if atualizar:
        carregar_visao_geral.clear()
        carregar_usuarios_basicos.clear()
        st.session_state["admin_visao_carregada"] = True

    if carregar:
        st.session_state["admin_visao_carregada"] = True

    if not st.session_state.get("admin_visao_carregada", False):
        st.info("Clique em **Carregar visão geral** para consultar o Firestore.")
        st.stop()

    with st.spinner("Carregando métricas..."):
        resumo = carregar_visao_geral()

    dados_usuarios = resumo["dados_usuarios"]
    total_acoes = resumo["total_acoes"]
    total_atividades_academicas = resumo["total_atividades_academicas"]
    usuarios_ativos_7dias = resumo["usuarios_ativos_7dias"]
    acoes_por_dia = resumo["acoes_por_dia"]
    acoes_por_tipo = resumo["acoes_por_tipo"]
    atividades_por_modulo = resumo["atividades_por_modulo"]
    atividades_por_tipo = resumo["atividades_por_tipo"]
    
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

elif secao == "👥 Usuários":
    st.header("Gerenciamento de Usuários")
    
    # Criar DataFrame com dados de usuários
    with st.spinner("Carregando usuários..."):
        df_usuarios = pd.DataFrame(carregar_usuarios_basicos())
    
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
        usuario_selecionado = st.selectbox(
            "Selecione um usuário para ver detalhes:",
            usuarios_emails,
            index=None,
            placeholder="Selecione um usuário",
            key="admin_select_user_details",
        )
        
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

elif secao == "🔍 Dados Detalhados":
    st.header("Dados Detalhados")
    st.write("Em desenvolvimento...")

    # Funcionalidade de download de dados (exemplo)
    df_usuarios = pd.DataFrame(carregar_usuarios_basicos())
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

elif secao == "📥 Exportar Dados":
    st.header("Exportar Dados (Excel)")
    st.caption("Nada é executado automaticamente: clique para iniciar a coleta e gerar o arquivo.")

    exportar = st.button("Exportar dados para Excel", type="primary")

    if exportar:
        # Parâmetros (fixos) da coleta detalhada
        incluir_contagens_por_tipo = True
        metricas_avancadas = True
        contar_mensagens_chat = False

        tempo_placeholder = st.empty()
        inicio = time.time()

        with st.spinner("Lendo dados do servidor e consolidando..."):
            usuarios_docs = db.collection(COLECAO_USUARIOS).get()

            linhas = []
            todos_tipos_acao = set()
            todos_tipos_atividade = set()

            for usuario_doc in usuarios_docs:
                # Atualiza contador de tempo
                decorrido = int(time.time() - inicio)
                tempo_placeholder.info(f"Tempo decorrido: {decorrido}s")

                dados_usuario = usuario_doc.to_dict() or {}
                email = dados_usuario.get("email", usuario_doc.id)

                # Coletas básicas do doc do usuário
                nome = (
                    dados_usuario.get("nome_completo")
                    or dados_usuario.get("nome_google")
                    or dados_usuario.get("nome")
                    or ""
                )
                curso = dados_usuario.get("curso", "")
                data_cadastro = dados_usuario.get("data_cadastro")
                ultimo_acesso = dados_usuario.get("ultimo_acesso")

                # Subcoleções
                usuario_ref = db.collection(COLECAO_USUARIOS).document(email)

                # Logs (ações)
                contagem_acoes = {}
                dias_ativos_set = set()
                primeiro_log_dt = None
                ultimo_log_dt = None
                total_acoes = 0
                try:
                    if incluir_contagens_por_tipo:
                        for log in usuario_ref.collection("logs").select(["acao", "data_hora"]).stream():
                            ld = log.to_dict() or {}
                            tipo = ld.get("acao", "Desconhecida")
                            dt = ld.get("data_hora")
                            contagem_acoes[tipo] = contagem_acoes.get(tipo, 0) + 1
                            if dt:
                                if not primeiro_log_dt or dt < primeiro_log_dt:
                                    primeiro_log_dt = dt
                                if not ultimo_log_dt or dt > ultimo_log_dt:
                                    ultimo_log_dt = dt
                                try:
                                    dias_ativos_set.add(dt.date())
                                except Exception:
                                    pass
                        total_acoes = sum(contagem_acoes.values())
                    else:
                        try:
                            agg = usuario_ref.collection("logs").count().get()
                            total_acoes = agg[0].value if agg else 0
                        except Exception:
                            total_acoes = len(list(usuario_ref.collection("logs").select(["__name__"]).stream()))
                        try:
                            first_q = list(usuario_ref.collection("logs").order_by("data_hora").limit(1).select(["data_hora"]).get())
                            if first_q:
                                primeiro_log_dt = first_q[0].to_dict().get("data_hora")
                            last_q = list(usuario_ref.collection("logs").order_by("data_hora", direction=firestore.Query.DESCENDING).limit(1).select(["data_hora"]).get())
                            if last_q:
                                ultimo_log_dt = last_q[0].to_dict().get("data_hora")
                        except Exception:
                            pass
                except Exception:
                    pass
                todos_tipos_acao.update(contagem_acoes.keys())

                # Atividades acadêmicas
                contagem_atividades = {}
                primeira_atividade_dt = None
                ultima_atividade_dt = None
                total_atividades = 0
                # Métricas avançadas
                aulas_licoes_vistas = set()
                chatbot_perguntas = 0
                chatbot_total_chars = 0
                quiz_tentativas = 0
                quiz_media_acerto_sum = 0.0
                prova_geradas = 0
                prova_concluidas = 0
                prova_media_acerto_sum = 0.0
                corretor_visualizacoes = 0
                corretor_avaliacoes = 0
                recurso_downloads = 0
                recursos_acessos = 0
                forum_posts = 0
                forum_likes_add = 0
                forum_likes_remove = 0

                try:
                    if incluir_contagens_por_tipo or metricas_avancadas:
                        for at in usuario_ref.collection("atividades_academicas").select(["tipo", "data_hora", "modulo", "detalhes"]).stream():
                            ad = at.to_dict() or {}
                            tipo = ad.get("tipo", "Desconhecida")
                            dt = ad.get("data_hora")
                            contagem_atividades[tipo] = contagem_atividades.get(tipo, 0) + 1
                            total_atividades += 1
                            if dt:
                                if not primeira_atividade_dt or dt < primeira_atividade_dt:
                                    primeira_atividade_dt = dt
                                if not ultima_atividade_dt or dt > ultima_atividade_dt:
                                    ultima_atividade_dt = dt
                                try:
                                    dias_ativos_set.add(dt.date())
                                except Exception:
                                    pass

                            if metricas_avancadas:
                                detalhes = ad.get("detalhes", {}) or {}
                                if tipo == "aula":
                                    licao = detalhes.get("licao")
                                    modulo_nome = ad.get("modulo")
                                    if licao and modulo_nome:
                                        aulas_licoes_vistas.add((modulo_nome, licao))
                                elif tipo == "chatbot":
                                    if detalhes.get("acao") == "pergunta":
                                        chatbot_perguntas += 1
                                        try:
                                            chatbot_total_chars += int(detalhes.get("tamanho_pergunta", 0))
                                        except Exception:
                                            pass
                                elif tipo == "quiz":
                                    try:
                                        quiz_tentativas += 1
                                        if "percentual_acerto" in detalhes:
                                            quiz_media_acerto_sum += float(detalhes.get("percentual_acerto") or 0.0)
                                    except Exception:
                                        pass
                                elif tipo == "avaliacao":
                                    acao = (detalhes.get("acao") or "").lower()
                                    if acao == "geracao_prova":
                                        prova_geradas += 1
                                    elif acao == "conclusao_prova":
                                        prova_concluidas += 1
                                        try:
                                            prova_media_acerto_sum += float(detalhes.get("percentual_acerto") or 0.0)
                                        except Exception:
                                            pass
                                elif tipo == "exercicio_corretor_ai":
                                    acao = detalhes.get("acao")
                                    if acao == "visualizacao_exercicio":
                                        corretor_visualizacoes += 1
                                    elif acao == "avaliacao_resposta_ia":
                                        corretor_avaliacoes += 1
                                elif tipo == "recurso_download":
                                    recurso_downloads += 1
                                elif tipo == "recursos":
                                    recursos_acessos += 1
                                elif tipo == "forum":
                                    acao = (detalhes.get("acao") or "").lower()
                                    if acao == "criar_post":
                                        forum_posts += 1
                                    elif acao == "adicionar_like":
                                        forum_likes_add += 1
                                    elif acao == "remover_like":
                                        forum_likes_remove += 1

                    else:
                        try:
                            agg = usuario_ref.collection("atividades_academicas").count().get()
                            total_atividades = agg[0].value if agg else 0
                        except Exception:
                            total_atividades = len(list(usuario_ref.collection("atividades_academicas").select(["__name__"]).stream()))
                        try:
                            first_q = list(usuario_ref.collection("atividades_academicas").order_by("data_hora").limit(1).select(["data_hora"]).get())
                            if first_q:
                                primeira_atividade_dt = first_q[0].to_dict().get("data_hora")
                            last_q = list(usuario_ref.collection("atividades_academicas").order_by("data_hora", direction=firestore.Query.DESCENDING).limit(1).select(["data_hora"]).get())
                            if last_q:
                                ultima_atividade_dt = last_q[0].to_dict().get("data_hora")
                        except Exception:
                            pass
                except Exception:
                    pass
                todos_tipos_atividade.update(contagem_atividades.keys())

                # Chats
                total_chats = 0
                total_mensagens_chat = 0
                primeira_interacao_chat_dt = None
                ultima_interacao_chat_dt = None
                try:
                    try:
                        agg = usuario_ref.collection("chats").count().get()
                        total_chats = agg[0].value if agg else 0
                    except Exception:
                        total_chats = len(list(usuario_ref.collection("chats").select(["__name__"]).stream()))

                    try:
                        first_chat = list(usuario_ref.collection("chats").order_by("data_criacao").limit(1).select(["data_criacao"]).get())
                        if first_chat:
                            primeira_interacao_chat_dt = first_chat[0].to_dict().get("data_criacao")
                            try:
                                dias_ativos_set.add(primeira_interacao_chat_dt.date())
                            except Exception:
                                pass
                        last_chat = list(usuario_ref.collection("chats").order_by("ultima_atualizacao", direction=firestore.Query.DESCENDING).limit(1).select(["ultima_atualizacao"]).get())
                        if last_chat:
                            ultima_interacao_chat_dt = last_chat[0].to_dict().get("ultima_atualizacao")
                            try:
                                dias_ativos_set.add(ultima_interacao_chat_dt.date())
                            except Exception:
                                pass
                    except Exception:
                        pass

                    if contar_mensagens_chat and total_chats:
                        for ch in usuario_ref.collection("chats").select(["numero_mensagens", "mensagens"]).stream():
                            chd = ch.to_dict() or {}
                            num_msgs = chd.get("numero_mensagens")
                            if isinstance(num_msgs, int):
                                total_mensagens_chat += num_msgs
                            elif isinstance(chd.get("mensagens"), list):
                                total_mensagens_chat += len(chd.get("mensagens", []))
                except Exception:
                    pass

                # Linha base
                linha = {
                    "Email": email,
                    "Nome": nome,
                    "Curso": curso,
                    "Data Cadastro": data_cadastro.strftime('%d/%m/%Y %H:%M:%S') if data_cadastro else "",
                    "Último Acesso": ultimo_acesso.strftime('%d/%m/%Y %H:%M:%S') if ultimo_acesso else "",
                    "Primeiro Log": primeiro_log_dt.strftime('%d/%m/%Y %H:%M:%S') if primeiro_log_dt else "",
                    "Último Log": ultimo_log_dt.strftime('%d/%m/%Y %H:%M:%S') if ultimo_log_dt else "",
                    "Primeira Atividade": primeira_atividade_dt.strftime('%d/%m/%Y %H:%M:%S') if primeira_atividade_dt else "",
                    "Última Atividade": ultima_atividade_dt.strftime('%d/%m/%Y %H:%M:%S') if ultima_atividade_dt else "",
                    "Primeira Interação Chat": primeira_interacao_chat_dt.strftime('%d/%m/%Y %H:%M:%S') if primeira_interacao_chat_dt else "",
                    "Última Interação Chat": ultima_interacao_chat_dt.strftime('%d/%m/%Y %H:%M:%S') if ultima_interacao_chat_dt else "",
                    "Dias Ativos": len(dias_ativos_set) if incluir_contagens_por_tipo else "",
                    "Total Ações": total_acoes,
                    "Total Atividades": total_atividades,
                    "Total Chats": total_chats,
                    "Total Mensagens Chat": total_mensagens_chat,
                }

                linha["_contagem_acoes"] = contagem_acoes
                linha["_contagem_atividades"] = contagem_atividades

                if metricas_avancadas:
                    linha["Aulas - Lições Únicas"] = len(aulas_licoes_vistas)
                    linha["Chatbot - Perguntas"] = chatbot_perguntas
                    linha["Chatbot - Total Caracteres Perguntas"] = chatbot_total_chars
                    linha["Quiz - Tentativas"] = quiz_tentativas
                    linha["Quiz - Média Acerto (%)"] = round(quiz_media_acerto_sum / quiz_tentativas, 2) if quiz_tentativas else 0.0
                    linha["Prova - Geradas"] = prova_geradas
                    linha["Prova - Concluídas"] = prova_concluidas
                    linha["Prova - Média Acerto (%)"] = round(prova_media_acerto_sum / prova_concluidas, 2) if prova_concluidas else 0.0
                    linha["Corretor AI - Visualizações"] = corretor_visualizacoes
                    linha["Corretor AI - Avaliações"] = corretor_avaliacoes
                    linha["Recursos - Downloads"] = recurso_downloads
                    linha["Recursos - Acessos Externos"] = recursos_acessos
                    linha["Fórum - Posts"] = forum_posts
                    linha["Fórum - Likes Dados"] = forum_likes_add
                    linha["Fórum - Likes Removidos"] = forum_likes_remove
                linhas.append(linha)

            # Expandir colunas dinâmicas (ações e atividades)
            col_acoes = sorted([f"Ação: {t}" for t in todos_tipos_acao]) if incluir_contagens_por_tipo else []
            col_ativs = sorted([f"Atividade: {t}" for t in todos_tipos_atividade]) if incluir_contagens_por_tipo else []

            linhas_expandidas = []
            for ln in linhas:
                nova = {k: v for k, v in ln.items() if not k.startswith("_")}
                cont_a = ln.get("_contagem_acoes", {})
                cont_at = ln.get("_contagem_atividades", {})
                for tcol in col_acoes:
                    tipo = tcol.replace("Ação: ", "")
                    nova[tcol] = cont_a.get(tipo, 0)
                for tcol in col_ativs:
                    tipo = tcol.replace("Atividade: ", "")
                    nova[tcol] = cont_at.get(tipo, 0)
                linhas_expandidas.append(nova)

            if linhas_expandidas:
                base_cols = [
                    "Email", "Nome", "Curso", "Data Cadastro", "Último Acesso",
                    "Primeiro Log", "Último Log", "Primeira Atividade", "Última Atividade",
                    "Primeira Interação Chat", "Última Interação Chat",
                    "Dias Ativos", "Total Ações", "Total Atividades", "Total Chats", "Total Mensagens Chat",
                ]
                outras_cols = [c for c in (col_acoes + col_ativs) if c not in base_cols]
                df_export = pd.DataFrame(linhas_expandidas)
                for c in base_cols + outras_cols:
                    if c not in df_export.columns:
                        df_export[c] = 0 if c not in {"Email", "Nome", "Curso", "Data Cadastro", "Último Acesso", "Primeiro Log", "Último Log", "Primeira Atividade", "Última Atividade", "Primeira Interação Chat", "Última Interação Chat"} else ""
                df_export = df_export[base_cols + outras_cols]

                # Gera Excel em memória
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df_export.to_excel(writer, index=False, sheet_name="Dados")
                buffer.seek(0)

                st.success("Exportação concluída!")
                st.download_button(
                    label="📥 Baixar Excel",
                    data=buffer.getvalue(),
                    file_name="export_usuarios_completo.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_export_excel"
                )
            else:
                st.info("Nenhum dado encontrado para exportação.")

st.divider()
st.page_link("paginas/chatbot.py", label=" Voltar para as conversas", icon="🏃", )
