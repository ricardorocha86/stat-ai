import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
from scipy.stats import norm, t, chi2
import seaborn as sns

# Configuração da página
st.set_page_config(
    page_title="Playground de Inferência Estatística",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração do estilo dos gráficos
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para Streamlit
plt.style.use('default')
sns.set_palette("husl")

# Função para criar gráficos com estilo limpo
def configurar_grafico():
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 14,
        'axes.titlesize': 16,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'figure.titlesize': 18
    })

# Navegação principal
def main():
    st.title("📊 Playground de Inferência Estatística")
    st.markdown("---")
    
    # Menu de navegação
    paginas = {
        "🔔 Distribuição Normal": pagina_distribuicao_normal,
        "📈 Distribuições Amostrais": pagina_distribuicoes_amostrais,
        "📊 Intervalo de Confiança": pagina_intervalo_confianca,
        "🧪 Testes de Hipóteses": pagina_testes_hipoteses,
        "📚 Referências em Nutrição": pagina_referencias_nutricao
    }
    
    pagina_selecionada = st.sidebar.selectbox("Selecione uma página:", list(paginas.keys()))
    
    # Executar a página selecionada
    paginas[pagina_selecionada]()

def pagina_distribuicao_normal():
    st.header("🔔 Calculadora da Distribuição Normal")
    
    # Teoria
    st.markdown("""
    ### 📘 Teoria
    > A distribuição normal é usada para modelar fenômenos contínuos. A área sob a curva representa uma probabilidade. 
    > Podemos calcular a chance de um valor ser menor, maior ou estar entre dois valores.
    """)
    
    # Exemplos didáticos
    with st.expander("📝 Exemplos Didáticos"):
        st.markdown("""
        **Farmácia:** Tempo de absorção de um medicamento segue N(90, 10²). Qual a chance de ser absorvido em menos de 75 minutos?
        
        **Nutrição:** O peso diário de consumo de sal segue N(6g, 1²). Qual a probabilidade de uma pessoa consumir entre 5g e 7g?
        
        **Outro:** O tempo de espera em um banco segue N(10 min, 2²). Qual a chance de esperar mais que 12 minutos?
        """)
    
    # Inputs
    col1, col2 = st.columns(2)
    
    with col1:
        media = st.number_input("Média (μ):", value=0.0, step=0.1)
        desvio_padrao = st.number_input("Desvio padrão (σ):", value=1.0, step=0.1, min_value=0.1)
        
    with col2:
        tipo_calculo = st.selectbox("Tipo de cálculo:", 
                                   ["P(X < x)", "P(X > x)", "P(a < X < b)"])
        
        if tipo_calculo in ["P(X < x)", "P(X > x)"]:
            valor_x = st.number_input("Valor x:", value=0.0, step=0.1)
        else:
            valor_a = st.number_input("Valor a:", value=-1.0, step=0.1)
            valor_b = st.number_input("Valor b:", value=1.0, step=0.1)
    
    # Cálculos
    if st.button("Calcular"):
        configurar_grafico()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Gerar dados para a curva
        x = np.linspace(media - 4*desvio_padrao, media + 4*desvio_padrao, 1000)
        y = norm.pdf(x, media, desvio_padrao)
        
        # Plotar a curva normal
        ax.plot(x, y, 'b-', linewidth=2, label='Distribuição Normal')
        
        # Calcular probabilidade e área sombreada
        if tipo_calculo == "P(X < x)":
            probabilidade = norm.cdf(valor_x, media, desvio_padrao)
            valor_z = (valor_x - media) / desvio_padrao
            
            # Área sombreada
            x_fill = x[x <= valor_x]
            y_fill = norm.pdf(x_fill, media, desvio_padrao)
            ax.fill_between(x_fill, y_fill, alpha=0.3, color='red', label=f'P(X < {valor_x})')
            
            # Linha vertical
            ax.axvline(valor_x, color='red', linestyle='--', linewidth=2)
            ax.annotate(f'x = {valor_x}', xy=(valor_x, 0), xytext=(valor_x, 0.05),
                       arrowprops=dict(arrowstyle='->', color='red'))
            
            resultado_texto = f"A probabilidade de X ser menor que {valor_x} é {probabilidade:.10f}"
            
        elif tipo_calculo == "P(X > x)":
            probabilidade = 1 - norm.cdf(valor_x, media, desvio_padrao)
            valor_z = (valor_x - media) / desvio_padrao
            
            # Área sombreada
            x_fill = x[x >= valor_x]
            y_fill = norm.pdf(x_fill, media, desvio_padrao)
            ax.fill_between(x_fill, y_fill, alpha=0.3, color='green', label=f'P(X > {valor_x})')
            
            # Linha vertical
            ax.axvline(valor_x, color='green', linestyle='--', linewidth=2)
            ax.annotate(f'x = {valor_x}', xy=(valor_x, 0), xytext=(valor_x, 0.05),
                       arrowprops=dict(arrowstyle='->', color='green'))
            
            resultado_texto = f"A probabilidade de X ser maior que {valor_x} é {probabilidade:.10f}"
            
        else:  # P(a < X < b)
            probabilidade = norm.cdf(valor_b, media, desvio_padrao) - norm.cdf(valor_a, media, desvio_padrao)
            valor_z_a = (valor_a - media) / desvio_padrao
            valor_z_b = (valor_b - media) / desvio_padrao
            
            # Área sombreada
            x_fill = x[(x >= valor_a) & (x <= valor_b)]
            y_fill = norm.pdf(x_fill, media, desvio_padrao)
            ax.fill_between(x_fill, y_fill, alpha=0.3, color='blue', label=f'P({valor_a} < X < {valor_b})')
            
            # Linhas verticais
            ax.axvline(valor_a, color='blue', linestyle='--', linewidth=2)
            ax.axvline(valor_b, color='blue', linestyle='--', linewidth=2)
            ax.annotate(f'a = {valor_a}', xy=(valor_a, 0), xytext=(valor_a, 0.05),
                       arrowprops=dict(arrowstyle='->', color='blue'))
            ax.annotate(f'b = {valor_b}', xy=(valor_b, 0), xytext=(valor_b, 0.05),
                       arrowprops=dict(arrowstyle='->', color='blue'))
            
            resultado_texto = f"A probabilidade de X estar entre {valor_a} e {valor_b} é {probabilidade:.10f}"
        
        ax.set_xlabel('Valores de X')
        ax.set_ylabel('Densidade de Probabilidade')
        ax.set_title(f'Distribuição Normal (μ={media}, σ={desvio_padrao})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # Resultados
        st.success(f"**Resultado:** {resultado_texto}")
        if tipo_calculo != "P(a < X < b)":
            st.info(f"**Valor Z correspondente:** {valor_z:.10f}")

def pagina_distribuicoes_amostrais():
    st.header("📈 Distribuições Amostrais")
    
    # Teoria
    st.markdown("""
    ### 📘 Teoria
    > Ao coletar muitas amostras, a distribuição das médias ou proporções amostrais se aproxima da normal, 
    > com média igual à da população e desvio padrão ajustado pelo tamanho da amostra.
    """)
    
    # Exemplos didáticos
    with st.expander("📝 Exemplos Didáticos"):
        st.markdown("""
        **Farmácia:** Tempo de liberação de um fármaco. Ver como a média de amostras varia.
        
        **Nutrição:** Proporção de pessoas que consomem fibras. Ver distribuição de p̂ com n=30.
        
        **Outro:** Idade média de clientes em um plano de saúde. Variações da média em amostras.
        """)
    
    # Inputs
    col1, col2 = st.columns(2)
    
    with col1:
        tipo_distribuicao = st.selectbox("Tipo:", ["Média", "Proporção"])
        tamanho_amostra = st.number_input("Tamanho da amostra (n):", value=30, min_value=5, max_value=1000)
        numero_simulacoes = st.number_input("Número de simulações:", value=1000, min_value=100, max_value=10000)
    
    with col2:
        if tipo_distribuicao == "Média":
            media_populacional = st.number_input("Média populacional (μ):", value=100.0, step=0.1)
            desvio_populacional = st.number_input("Desvio padrão populacional (σ):", value=15.0, step=0.1, min_value=0.1)
        else:
            proporcao_populacional = st.number_input("Proporção populacional (p):", value=0.5, min_value=0.01, max_value=0.99, step=0.01)
    
    # Simulação
    if st.button("Executar Simulação"):
        configurar_grafico()
        
        if tipo_distribuicao == "Média":
            # Simular médias amostrais
            medias_amostrais = []
            for _ in range(numero_simulacoes):
                amostra = np.random.normal(media_populacional, desvio_populacional, tamanho_amostra)
                medias_amostrais.append(np.mean(amostra))
            
            medias_amostrais = np.array(medias_amostrais)
            
            # Parâmetros teóricos
            media_teorica = media_populacional
            desvio_teorico = desvio_populacional / np.sqrt(tamanho_amostra)
            
            # Estatísticas simuladas
            media_simulada = np.mean(medias_amostrais)
            desvio_simulado = np.std(medias_amostrais)
            
            # Gráfico
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Histograma das médias simuladas
            ax.hist(medias_amostrais, bins=50, density=True, alpha=0.7, color='skyblue', 
                   label=f'Médias Simuladas (n={numero_simulacoes})')
            
            # Curva normal teórica
            x = np.linspace(medias_amostrais.min(), medias_amostrais.max(), 1000)
            y_teorica = norm.pdf(x, media_teorica, desvio_teorico)
            ax.plot(x, y_teorica, 'r-', linewidth=3, label='Distribuição Teórica')
            
            # Linhas verticais
            ax.axvline(media_teorica, color='red', linestyle='--', linewidth=2, label=f'Média Teórica: {media_teorica:.4f}')
            ax.axvline(media_simulada, color='blue', linestyle='--', linewidth=2, label=f'Média Simulada: {media_simulada:.4f}')
            
            ax.set_xlabel('Médias Amostrais')
            ax.set_ylabel('Densidade')
            ax.set_title(f'Distribuição Amostral da Média (n={tamanho_amostra})')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
            # Resultados
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Média Teórica", f"{media_teorica:.10f}")
                st.metric("Desvio Padrão Teórico", f"{desvio_teorico:.10f}")
            with col2:
                st.metric("Média Simulada", f"{media_simulada:.10f}")
                st.metric("Desvio Padrão Simulado", f"{desvio_simulado:.10f}")
        
        else:  # Proporção
            # Simular proporções amostrais
            proporcoes_amostrais = []
            for _ in range(numero_simulacoes):
                amostra = np.random.binomial(1, proporcao_populacional, tamanho_amostra)
                proporcoes_amostrais.append(np.mean(amostra))
            
            proporcoes_amostrais = np.array(proporcoes_amostrais)
            
            # Parâmetros teóricos
            media_teorica = proporcao_populacional
            desvio_teorico = np.sqrt(proporcao_populacional * (1 - proporcao_populacional) / tamanho_amostra)
            
            # Estatísticas simuladas
            media_simulada = np.mean(proporcoes_amostrais)
            desvio_simulado = np.std(proporcoes_amostrais)
            
            # Gráfico
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Histograma das proporções simuladas
            ax.hist(proporcoes_amostrais, bins=50, density=True, alpha=0.7, color='lightgreen', 
                   label=f'Proporções Simuladas (n={numero_simulacoes})')
            
            # Curva normal teórica
            x = np.linspace(proporcoes_amostrais.min(), proporcoes_amostrais.max(), 1000)
            y_teorica = norm.pdf(x, media_teorica, desvio_teorico)
            ax.plot(x, y_teorica, 'r-', linewidth=3, label='Distribuição Teórica')
            
            # Linhas verticais
            ax.axvline(media_teorica, color='red', linestyle='--', linewidth=2, label=f'Proporção Teórica: {media_teorica:.4f}')
            ax.axvline(media_simulada, color='green', linestyle='--', linewidth=2, label=f'Proporção Simulada: {media_simulada:.4f}')
            
            ax.set_xlabel('Proporções Amostrais')
            ax.set_ylabel('Densidade')
            ax.set_title(f'Distribuição Amostral da Proporção (n={tamanho_amostra})')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
            # Resultados
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Proporção Teórica", f"{media_teorica:.10f}")
                st.metric("Desvio Padrão Teórico", f"{desvio_teorico:.10f}")
            with col2:
                st.metric("Proporção Simulada", f"{media_simulada:.10f}")
                st.metric("Desvio Padrão Simulado", f"{desvio_simulado:.10f}")

def pagina_intervalo_confianca():
    st.header("📊 Intervalo de Confiança")
    
    # Teoria
    st.markdown("""
    ### 📘 Teoria
    > Intervalos de confiança fornecem uma estimativa da localização do parâmetro populacional (média ou proporção), 
    > com base na variabilidade da amostra.
    """)
    
    # Abas
    aba_media, aba_proporcao = st.tabs(["📈 IC para a Média", "📊 IC para a Proporção"])
    
    with aba_media:
        st.subheader("Intervalo de Confiança para a Média")
        
        # Exemplos
        with st.expander("📝 Exemplos Didáticos"):
            st.markdown("""
            **Farmácia:** A média de dosagens administradas foi 98mg. Calcular IC.
            
            **Nutrição:** Estimar a média de calorias ingeridas por crianças com 95% de confiança.
            
            **Outro:** Tempo médio de atendimento em hospital. Estimar com base em amostra.
            """)
        
        # Inputs
        col1, col2 = st.columns(2)
        
        with col1:
            media_amostral = st.number_input("Média amostral (x̄):", value=100.0, step=0.1)
            desvio_amostral = st.number_input("Desvio padrão amostral (s):", value=15.0, step=0.1, min_value=0.1)
            
        with col2:
            tamanho_amostra_ic = st.number_input("Tamanho da amostra (n):", value=25, min_value=2)
            nivel_confianca = st.selectbox("Nível de confiança:", [90, 95, 99])
            
        # Valor hipotético opcional
        usar_mu0 = st.checkbox("Incluir valor hipotético μ₀ no gráfico")
        if usar_mu0:
            mu0 = st.number_input("Valor hipotético (μ₀):", value=105.0, step=0.1)
        
        if st.button("Calcular IC para Média"):
            # Cálculos
            alpha = (100 - nivel_confianca) / 100
            graus_liberdade = tamanho_amostra_ic - 1
            t_critico = t.ppf(1 - alpha/2, graus_liberdade)
            
            erro_padrao = desvio_amostral / np.sqrt(tamanho_amostra_ic)
            margem_erro = t_critico * erro_padrao
            
            limite_inferior = media_amostral - margem_erro
            limite_superior = media_amostral + margem_erro
            
            # Gráfico
            configurar_grafico()
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Linha do intervalo
            ax.plot([limite_inferior, limite_superior], [0.5, 0.5], 'b-', linewidth=8, alpha=0.7, label=f'IC {nivel_confianca}%')
            ax.plot(media_amostral, 0.5, 'ro', markersize=12, label=f'x̄ = {media_amostral}')
            
            # Margens com hachuras
            ax.fill_between([limite_inferior, media_amostral], 0.4, 0.6, alpha=0.3, color='blue', hatch='///')
            ax.fill_between([media_amostral, limite_superior], 0.4, 0.6, alpha=0.3, color='blue', hatch='///')
            
            # Anotações
            ax.annotate(f'LI = {limite_inferior:.4f}', xy=(limite_inferior, 0.5), xytext=(limite_inferior, 0.7),
                       arrowprops=dict(arrowstyle='->', color='blue'), ha='center')
            ax.annotate(f'LS = {limite_superior:.4f}', xy=(limite_superior, 0.5), xytext=(limite_superior, 0.7),
                       arrowprops=dict(arrowstyle='->', color='blue'), ha='center')
            
            # Valor hipotético se especificado
            if usar_mu0:
                ax.plot(mu0, 0.5, 'gs', markersize=12, label=f'μ₀ = {mu0}')
                if limite_inferior <= mu0 <= limite_superior:
                    resultado_hipotese = "μ₀ está DENTRO do intervalo"
                    cor_resultado = "green"
                else:
                    resultado_hipotese = "μ₀ está FORA do intervalo"
                    cor_resultado = "red"
                ax.text(0.5, 0.9, resultado_hipotese, transform=ax.transAxes, 
                       fontsize=14, ha='center', color=cor_resultado, weight='bold')
            
            ax.set_ylim(0.3, 1.0)
            ax.set_xlabel('Valores')
            ax.set_title(f'Intervalo de Confiança {nivel_confianca}% para a Média')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
            # Resultados
            st.success(f"**Intervalo de Confiança {nivel_confianca}%:** [{limite_inferior:.10f}, {limite_superior:.10f}]")
            st.info(f"**Margem de Erro:** {margem_erro:.10f}")
            st.info(f"**Valor t crítico:** {t_critico:.10f}")
    
    with aba_proporcao:
        st.subheader("Intervalo de Confiança para a Proporção")
        
        # Exemplos
        with st.expander("📝 Exemplos Didáticos"):
            st.markdown("""
            **Farmácia:** Proporção de pacientes que tiveram efeito colateral.
            
            **Nutrição:** Percentual de pessoas que consomem refrigerantes diariamente.
            
            **Outro:** Proporção de eleitores indecisos numa pesquisa.
            """)
        
        # Inputs
        col1, col2 = st.columns(2)
        
        with col1:
            sucessos = st.number_input("Número de sucessos (x):", value=45, min_value=0)
            tamanho_amostra_prop = st.number_input("Tamanho da amostra (n):", value=100, min_value=1)
            
        with col2:
            nivel_confianca_prop = st.selectbox("Nível de confiança:", [90, 95, 99], key="prop_conf")
        
        if st.button("Calcular IC para Proporção"):
            # Cálculos
            proporcao_amostral = sucessos / tamanho_amostra_prop
            alpha = (100 - nivel_confianca_prop) / 100
            z_critico = norm.ppf(1 - alpha/2)
            
            erro_padrao_prop = np.sqrt(proporcao_amostral * (1 - proporcao_amostral) / tamanho_amostra_prop)
            margem_erro_prop = z_critico * erro_padrao_prop
            
            limite_inferior_prop = max(0, proporcao_amostral - margem_erro_prop)
            limite_superior_prop = min(1, proporcao_amostral + margem_erro_prop)
            
            # Gráfico
            configurar_grafico()
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Linha do intervalo
            ax.plot([limite_inferior_prop, limite_superior_prop], [0.5, 0.5], 'g-', linewidth=8, alpha=0.7, 
                   label=f'IC {nivel_confianca_prop}%')
            ax.plot(proporcao_amostral, 0.5, 'ro', markersize=12, label=f'p̂ = {proporcao_amostral:.4f}')
            
            # Margens com hachuras
            ax.fill_between([limite_inferior_prop, proporcao_amostral], 0.4, 0.6, alpha=0.3, color='green', hatch='///')
            ax.fill_between([proporcao_amostral, limite_superior_prop], 0.4, 0.6, alpha=0.3, color='green', hatch='///')
            
            # Anotações com setas
            ax.annotate(f'LI = {limite_inferior_prop:.4f}', xy=(limite_inferior_prop, 0.5), xytext=(limite_inferior_prop, 0.7),
                       arrowprops=dict(arrowstyle='->', color='green'), ha='center')
            ax.annotate(f'LS = {limite_superior_prop:.4f}', xy=(limite_superior_prop, 0.5), xytext=(limite_superior_prop, 0.7),
                       arrowprops=dict(arrowstyle='->', color='green'), ha='center')
            
            ax.set_ylim(0.3, 1.0)
            ax.set_xlim(max(0, limite_inferior_prop - 0.1), min(1, limite_superior_prop + 0.1))
            ax.set_xlabel('Proporção')
            ax.set_title(f'Intervalo de Confiança {nivel_confianca_prop}% para a Proporção')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
            # Resultados
            st.success(f"**Intervalo de Confiança {nivel_confianca_prop}%:** [{limite_inferior_prop:.10f}, {limite_superior_prop:.10f}]")
            st.info(f"**Proporção Amostral:** {proporcao_amostral:.10f}")
            st.info(f"**Margem de Erro:** {margem_erro_prop:.10f}")
            st.info(f"**Valor z crítico:** {z_critico:.10f}")

def pagina_testes_hipoteses():
    st.header("🧪 Testes de Hipóteses")
    
    # Teoria
    st.markdown("""
    ### 📘 Teoria
    > Os testes de hipótese verificam se uma evidência amostral é forte o suficiente para rejeitar uma suposição sobre a população.
    """)
    
    # Abas
    aba_media, aba_proporcao, aba_diferenca = st.tabs(["📈 Teste para Média", "📊 Teste para Proporção", "⚖️ Diferença de Médias"])
    
    with aba_media:
        st.subheader("Teste de Hipótese para a Média")
        
        # Exemplos
        with st.expander("📝 Exemplos Didáticos"):
            st.markdown("""
            **Farmácia:** Testar se a concentração média do remédio difere de 100mg.
            
            **Nutrição:** Verificar se o consumo médio de açúcar é maior que 50g.
            
            **Outro:** Salário médio dos funcionários é diferente de R$3000?
            """)
        
        # Inputs
        col1, col2 = st.columns(2)
        
        with col1:
            media_amostral_teste = st.number_input("Média amostral (x̄):", value=102.0, step=0.1, key="teste_media")
            desvio_amostral_teste = st.number_input("Desvio padrão amostral (s):", value=12.0, step=0.1, min_value=0.1, key="teste_desvio")
            tamanho_amostra_teste = st.number_input("Tamanho da amostra (n):", value=25, min_value=2, key="teste_n")
            
        with col2:
            mu0_teste = st.number_input("Valor hipotético (μ₀):", value=100.0, step=0.1, key="teste_mu0")
            alpha_teste = st.selectbox("Nível de significância (α):", [0.01, 0.05, 0.10], key="teste_alpha")
            tipo_teste = st.selectbox("Tipo de teste:", ["Bilateral", "Unilateral à direita", "Unilateral à esquerda"], key="teste_tipo")
        
        if st.button("Executar Teste para Média"):
            # Cálculos
            graus_liberdade_teste = tamanho_amostra_teste - 1
            erro_padrao_teste = desvio_amostral_teste / np.sqrt(tamanho_amostra_teste)
            estatistica_t = (media_amostral_teste - mu0_teste) / erro_padrao_teste
            
            # Valores críticos e p-valor
            if tipo_teste == "Bilateral":
                t_critico_inf = t.ppf(alpha_teste/2, graus_liberdade_teste)
                t_critico_sup = t.ppf(1 - alpha_teste/2, graus_liberdade_teste)
                p_valor = 2 * (1 - t.cdf(abs(estatistica_t), graus_liberdade_teste))
                regiao_rejeicao = f"t < {t_critico_inf:.4f} ou t > {t_critico_sup:.4f}"
            elif tipo_teste == "Unilateral à direita":
                t_critico_sup = t.ppf(1 - alpha_teste, graus_liberdade_teste)
                p_valor = 1 - t.cdf(estatistica_t, graus_liberdade_teste)
                regiao_rejeicao = f"t > {t_critico_sup:.4f}"
            else:  # Unilateral à esquerda
                t_critico_inf = t.ppf(alpha_teste, graus_liberdade_teste)
                p_valor = t.cdf(estatistica_t, graus_liberdade_teste)
                regiao_rejeicao = f"t < {t_critico_inf:.4f}"
            
            # Decisão
            if p_valor < alpha_teste:
                decisao = "Rejeitamos H₀"
                cor_decisao = "red"
            else:
                decisao = "Não rejeitamos H₀"
                cor_decisao = "green"
            
            # Gráfico
            configurar_grafico()
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Curva t
            x = np.linspace(-4, 4, 1000)
            y = t.pdf(x, graus_liberdade_teste)
            ax.plot(x, y, 'b-', linewidth=2, label='Distribuição t')
            
            # Áreas críticas
            if tipo_teste == "Bilateral":
                x_crit_inf = x[x <= t_critico_inf]
                y_crit_inf = t.pdf(x_crit_inf, graus_liberdade_teste)
                ax.fill_between(x_crit_inf, y_crit_inf, alpha=0.3, color='red', hatch='///', label='Região de Rejeição')
                
                x_crit_sup = x[x >= t_critico_sup]
                y_crit_sup = t.pdf(x_crit_sup, graus_liberdade_teste)
                ax.fill_between(x_crit_sup, y_crit_sup, alpha=0.3, color='red', hatch='///')
                
                ax.axvline(t_critico_inf, color='red', linestyle='--', linewidth=2)
                ax.axvline(t_critico_sup, color='red', linestyle='--', linewidth=2)
                
            elif tipo_teste == "Unilateral à direita":
                x_crit = x[x >= t_critico_sup]
                y_crit = t.pdf(x_crit, graus_liberdade_teste)
                ax.fill_between(x_crit, y_crit, alpha=0.3, color='red', hatch='///', label='Região de Rejeição')
                ax.axvline(t_critico_sup, color='red', linestyle='--', linewidth=2)
                
            else:  # Unilateral à esquerda
                x_crit = x[x <= t_critico_inf]
                y_crit = t.pdf(x_crit, graus_liberdade_teste)
                ax.fill_between(x_crit, y_crit, alpha=0.3, color='red', hatch='///', label='Região de Rejeição')
                ax.axvline(t_critico_inf, color='red', linestyle='--', linewidth=2)
            
            # Estatística observada
            ax.axvline(estatistica_t, color='orange', linewidth=3, label=f't observado = {estatistica_t:.4f}')
            ax.annotate(f't = {estatistica_t:.4f}', xy=(estatistica_t, 0), xytext=(estatistica_t, 0.1),
                       arrowprops=dict(arrowstyle='->', color='orange'), ha='center')
            
            # Área do p-valor
            if tipo_teste == "Bilateral":
                if estatistica_t > 0:
                    x_p = x[x >= estatistica_t]
                    y_p = t.pdf(x_p, graus_liberdade_teste)
                    ax.fill_between(x_p, y_p, alpha=0.5, color='yellow', label=f'p-valor/2 = {p_valor/2:.6f}')
                    x_p2 = x[x <= -estatistica_t]
                    y_p2 = t.pdf(x_p2, graus_liberdade_teste)
                    ax.fill_between(x_p2, y_p2, alpha=0.5, color='yellow')
                else:
                    x_p = x[x <= estatistica_t]
                    y_p = t.pdf(x_p, graus_liberdade_teste)
                    ax.fill_between(x_p, y_p, alpha=0.5, color='yellow', label=f'p-valor/2 = {p_valor/2:.6f}')
                    x_p2 = x[x >= -estatistica_t]
                    y_p2 = t.pdf(x_p2, graus_liberdade_teste)
                    ax.fill_between(x_p2, y_p2, alpha=0.5, color='yellow')
            elif tipo_teste == "Unilateral à direita":
                x_p = x[x >= estatistica_t]
                y_p = t.pdf(x_p, graus_liberdade_teste)
                ax.fill_between(x_p, y_p, alpha=0.5, color='yellow', label=f'p-valor = {p_valor:.6f}')
            else:
                x_p = x[x <= estatistica_t]
                y_p = t.pdf(x_p, graus_liberdade_teste)
                ax.fill_between(x_p, y_p, alpha=0.5, color='yellow', label=f'p-valor = {p_valor:.6f}')
            
            ax.set_xlabel('Valores de t')
            ax.set_ylabel('Densidade')
            ax.set_title(f'Teste de Hipótese para a Média ({tipo_teste})')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
            # Resultados
            st.success(f"**Estatística t observada:** {estatistica_t:.10f}")
            st.success(f"**p-valor:** {p_valor:.10f}")
            st.success(f"**Região de rejeição:** {regiao_rejeicao}")
            
            if p_valor < alpha_teste:
                st.error(f"**Decisão:** {decisao} (p = {p_valor:.10f} < {alpha_teste})")
            else:
                st.info(f"**Decisão:** {decisao} (p = {p_valor:.10f} ≥ {alpha_teste})")
    
    with aba_proporcao:
        st.subheader("Teste de Hipótese para a Proporção")
        
        # Exemplos
        with st.expander("📝 Exemplos Didáticos"):
            st.markdown("""
            **Farmácia:** Mais de 10% dos pacientes têm reações adversas?
            
            **Nutrição:** Menos de 20% dos alunos comem vegetais diariamente?
            
            **Outro:** Proporção de aprovação no vestibular é 50%?
            """)
        
        # Inputs
        col1, col2 = st.columns(2)
        
        with col1:
            sucessos_teste = st.number_input("Número de sucessos (x):", value=55, min_value=0, key="prop_sucessos")
            tamanho_amostra_prop_teste = st.number_input("Tamanho da amostra (n):", value=200, min_value=1, key="prop_n")
            
        with col2:
            p0_teste = st.number_input("Proporção hipotética (p₀):", value=0.25, min_value=0.01, max_value=0.99, step=0.01, key="prop_p0")
            alpha_prop_teste = st.selectbox("Nível de significância (α):", [0.01, 0.05, 0.10], key="prop_alpha")
            tipo_teste_prop = st.selectbox("Tipo de teste:", ["Bilateral", "Unilateral à direita", "Unilateral à esquerda"], key="prop_tipo")
        
        if st.button("Executar Teste para Proporção"):
            # Cálculos
            proporcao_amostral_teste = sucessos_teste / tamanho_amostra_prop_teste
            erro_padrao_prop_teste = np.sqrt(p0_teste * (1 - p0_teste) / tamanho_amostra_prop_teste)
            estatistica_z = (proporcao_amostral_teste - p0_teste) / erro_padrao_prop_teste
            
            # Valores críticos e p-valor
            if tipo_teste_prop == "Bilateral":
                z_critico_inf = norm.ppf(alpha_prop_teste/2)
                z_critico_sup = norm.ppf(1 - alpha_prop_teste/2)
                p_valor_prop = 2 * (1 - norm.cdf(abs(estatistica_z)))
                regiao_rejeicao_prop = f"z < {z_critico_inf:.4f} ou z > {z_critico_sup:.4f}"
            elif tipo_teste_prop == "Unilateral à direita":
                z_critico_sup = norm.ppf(1 - alpha_prop_teste)
                p_valor_prop = 1 - norm.cdf(estatistica_z)
                regiao_rejeicao_prop = f"z > {z_critico_sup:.4f}"
            else:  # Unilateral à esquerda
                z_critico_inf = norm.ppf(alpha_prop_teste)
                p_valor_prop = norm.cdf(estatistica_z)
                regiao_rejeicao_prop = f"z < {z_critico_inf:.4f}"
            
            # Gráfico
            configurar_grafico()
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Curva normal padrão
            x = np.linspace(-4, 4, 1000)
            y = norm.pdf(x)
            ax.plot(x, y, 'b-', linewidth=2, label='Distribuição Normal Padrão')
            
            # Áreas críticas
            if tipo_teste_prop == "Bilateral":
                x_crit_inf = x[x <= z_critico_inf]
                y_crit_inf = norm.pdf(x_crit_inf)
                ax.fill_between(x_crit_inf, y_crit_inf, alpha=0.3, color='red', hatch='///', label='Região de Rejeição')
                
                x_crit_sup = x[x >= z_critico_sup]
                y_crit_sup = norm.pdf(x_crit_sup)
                ax.fill_between(x_crit_sup, y_crit_sup, alpha=0.3, color='red', hatch='///')
                
                ax.axvline(z_critico_inf, color='red', linestyle='--', linewidth=2)
                ax.axvline(z_critico_sup, color='red', linestyle='--', linewidth=2)
                
            elif tipo_teste_prop == "Unilateral à direita":
                x_crit = x[x >= z_critico_sup]
                y_crit = norm.pdf(x_crit)
                ax.fill_between(x_crit, y_crit, alpha=0.3, color='red', hatch='///', label='Região de Rejeição')
                ax.axvline(z_critico_sup, color='red', linestyle='--', linewidth=2)
                
            else:  # Unilateral à esquerda
                x_crit = x[x <= z_critico_inf]
                y_crit = norm.pdf(x_crit)
                ax.fill_between(x_crit, y_crit, alpha=0.3, color='red', hatch='///', label='Região de Rejeição')
                ax.axvline(z_critico_inf, color='red', linestyle='--', linewidth=2)
            
            # Estatística observada
            ax.axvline(estatistica_z, color='orange', linewidth=3, label=f'z observado = {estatistica_z:.4f}')
            ax.annotate(f'z = {estatistica_z:.4f}', xy=(estatistica_z, 0), xytext=(estatistica_z, 0.1),
                       arrowprops=dict(arrowstyle='->', color='orange'), ha='center')
            
            ax.set_xlabel('Valores de z')
            ax.set_ylabel('Densidade')
            ax.set_title(f'Teste de Hipótese para a Proporção ({tipo_teste_prop})')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
            # Resultados
            st.success(f"**Proporção amostral:** {proporcao_amostral_teste:.10f}")
            st.success(f"**Estatística z observada:** {estatistica_z:.10f}")
            st.success(f"**p-valor:** {p_valor_prop:.10f}")
            st.success(f"**Região de rejeição:** {regiao_rejeicao_prop}")
            
            if p_valor_prop < alpha_prop_teste:
                st.error(f"**Decisão:** Rejeitamos H₀ (p = {p_valor_prop:.10f} < {alpha_prop_teste})")
            else:
                st.info(f"**Decisão:** Não rejeitamos H₀ (p = {p_valor_prop:.10f} ≥ {alpha_prop_teste})")
    
    with aba_diferenca:
        st.subheader("Teste para Diferença de Médias")
        
        # Exemplos
        with st.expander("📝 Exemplos Didáticos"):
            st.markdown("""
            **Farmácia:** Comparar a eficácia de dois medicamentos.
            
            **Nutrição:** Comparar ingestão de sódio entre dois grupos.
            
            **Outro:** Comparar rendimento escolar de dois métodos de ensino.
            """)
        
        # Inputs
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Grupo 1:**")
            media1 = st.number_input("Média 1 (x̄₁):", value=105.0, step=0.1, key="dif_media1")
            desvio1 = st.number_input("Desvio padrão 1 (s₁):", value=12.0, step=0.1, min_value=0.1, key="dif_desvio1")
            n1 = st.number_input("Tamanho da amostra 1 (n₁):", value=25, min_value=2, key="dif_n1")
            
        with col2:
            st.markdown("**Grupo 2:**")
            media2 = st.number_input("Média 2 (x̄₂):", value=98.0, step=0.1, key="dif_media2")
            desvio2 = st.number_input("Desvio padrão 2 (s₂):", value=15.0, step=0.1, min_value=0.1, key="dif_desvio2")
            n2 = st.number_input("Tamanho da amostra 2 (n₂):", value=30, min_value=2, key="dif_n2")
        
        tipo_variancia = st.selectbox("Tipo de variâncias:", ["Iguais", "Diferentes", "Pareado"], key="dif_variancia")
        alpha_dif = st.selectbox("Nível de significância (α):", [0.01, 0.05, 0.10], key="dif_alpha")
        tipo_teste_dif = st.selectbox("Tipo de teste:", ["Bilateral", "Unilateral à direita", "Unilateral à esquerda"], key="dif_tipo")
        
        if st.button("Executar Teste para Diferença"):
            # Cálculos baseados no tipo de variância
            diferenca_medias = media1 - media2
            
            if tipo_variancia == "Iguais":
                # Variâncias iguais - pooled variance
                sp_squared = ((n1-1)*desvio1**2 + (n2-1)*desvio2**2) / (n1 + n2 - 2)
                erro_padrao_dif = np.sqrt(sp_squared * (1/n1 + 1/n2))
                graus_liberdade_dif = n1 + n2 - 2
                
            elif tipo_variancia == "Diferentes":
                # Variâncias diferentes - Welch's t-test
                erro_padrao_dif = np.sqrt(desvio1**2/n1 + desvio2**2/n2)
                # Graus de liberdade de Welch
                numerador = (desvio1**2/n1 + desvio2**2/n2)**2
                denominador = (desvio1**2/n1)**2/(n1-1) + (desvio2**2/n2)**2/(n2-1)
                graus_liberdade_dif = numerador / denominador
                
            else:  # Pareado
                # Para dados pareados, assumimos que temos as diferenças
                # Aqui simplificamos usando a diferença das médias
                erro_padrao_dif = np.sqrt(desvio1**2/n1)  # Simplificação
                graus_liberdade_dif = n1 - 1
            
            estatistica_t_dif = diferenca_medias / erro_padrao_dif
            
            # Valores críticos e p-valor
            if tipo_teste_dif == "Bilateral":
                t_critico_inf_dif = t.ppf(alpha_dif/2, graus_liberdade_dif)
                t_critico_sup_dif = t.ppf(1 - alpha_dif/2, graus_liberdade_dif)
                p_valor_dif = 2 * (1 - t.cdf(abs(estatistica_t_dif), graus_liberdade_dif))
            elif tipo_teste_dif == "Unilateral à direita":
                t_critico_sup_dif = t.ppf(1 - alpha_dif, graus_liberdade_dif)
                p_valor_dif = 1 - t.cdf(estatistica_t_dif, graus_liberdade_dif)
            else:  # Unilateral à esquerda
                t_critico_inf_dif = t.ppf(alpha_dif, graus_liberdade_dif)
                p_valor_dif = t.cdf(estatistica_t_dif, graus_liberdade_dif)
            
            # Gráfico
            configurar_grafico()
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Curva t
            x = np.linspace(-4, 4, 1000)
            y = t.pdf(x, graus_liberdade_dif)
            ax.plot(x, y, 'b-', linewidth=2, label='Distribuição t')
            
            # Áreas críticas
            if tipo_teste_dif == "Bilateral":
                x_crit_inf = x[x <= t_critico_inf_dif]
                y_crit_inf = t.pdf(x_crit_inf, graus_liberdade_dif)
                ax.fill_between(x_crit_inf, y_crit_inf, alpha=0.3, color='red', hatch='///', label='Região de Rejeição')
                
                x_crit_sup = x[x >= t_critico_sup_dif]
                y_crit_sup = t.pdf(x_crit_sup, graus_liberdade_dif)
                ax.fill_between(x_crit_sup, y_crit_sup, alpha=0.3, color='red', hatch='///')
                
                ax.axvline(t_critico_inf_dif, color='red', linestyle='--', linewidth=2)
                ax.axvline(t_critico_sup_dif, color='red', linestyle='--', linewidth=2)
                
            elif tipo_teste_dif == "Unilateral à direita":
                x_crit = x[x >= t_critico_sup_dif]
                y_crit = t.pdf(x_crit, graus_liberdade_dif)
                ax.fill_between(x_crit, y_crit, alpha=0.3, color='red', hatch='///', label='Região de Rejeição')
                ax.axvline(t_critico_sup_dif, color='red', linestyle='--', linewidth=2)
                
            else:  # Unilateral à esquerda
                x_crit = x[x <= t_critico_inf_dif]
                y_crit = t.pdf(x_crit, graus_liberdade_dif)
                ax.fill_between(x_crit, y_crit, alpha=0.3, color='red', hatch='///', label='Região de Rejeição')
                ax.axvline(t_critico_inf_dif, color='red', linestyle='--', linewidth=2)
            
            # Estatística observada
            ax.axvline(estatistica_t_dif, color='orange', linewidth=3, label=f't observado = {estatistica_t_dif:.4f}')
            ax.annotate(f't = {estatistica_t_dif:.4f}', xy=(estatistica_t_dif, 0), xytext=(estatistica_t_dif, 0.1),
                       arrowprops=dict(arrowstyle='->', color='orange'), ha='center')
            
            ax.set_xlabel('Valores de t')
            ax.set_ylabel('Densidade')
            ax.set_title(f'Teste para Diferença de Médias ({tipo_teste_dif}) - {tipo_variancia}')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
            # Resultados
            st.success(f"**Diferença das médias (x̄₁ - x̄₂):** {diferenca_medias:.10f}")
            st.success(f"**Erro padrão da diferença:** {erro_padrao_dif:.10f}")
            st.success(f"**Graus de liberdade:** {graus_liberdade_dif:.2f}")
            st.success(f"**Estatística t observada:** {estatistica_t_dif:.10f}")
            st.success(f"**p-valor:** {p_valor_dif:.10f}")
            
            if p_valor_dif < alpha_dif:
                st.error(f"**Decisão:** Rejeitamos H₀ (p = {p_valor_dif:.10f} < {alpha_dif})")
            else:
                st.info(f"**Decisão:** Não rejeitamos H₀ (p = {p_valor_dif:.10f} ≥ {alpha_dif})")

def pagina_referencias_nutricao():
    st.header("📚 Referências em Nutrição")
    
    st.markdown("""
    ### 📖 Artigos Científicos Famosos e Relevantes na Área de Nutrição
    
    Esta seção apresenta uma seleção de estudos seminais e influentes que moldaram nossa compreensão atual sobre nutrição e saúde.
    """)
    
    # Artigo 1
    st.markdown("---")
    st.subheader("1. 🥗 Alimentos Ultraprocessados e Ganho de Peso")
    
    with st.expander("📄 Detalhes do Estudo"):
        st.markdown("""
        **Título:** Ultra-Processed Diets Cause Excess Calorie Intake and Weight Gain: An Inpatient Randomized Controlled Trial of Ad Libitum Food Intake
        
        **Autores:** Kevin D. Hall, Alexis Ayuketah, Robert Brychta, et al.
        
        **Revista:** Cell Metabolism, 2019
        
        **Resumo:** Este estudo controlado randomizado foi o primeiro a demonstrar causalmente que alimentos ultraprocessados levam ao aumento do consumo calórico e ganho de peso. Participantes consumiram 508 kcal/dia a mais quando expostos à dieta ultraprocessada comparada à dieta não processada, resultando em ganho de 0,9 kg em duas semanas.
        
        **Importância:** Forneceu evidência causal direta sobre os efeitos dos alimentos ultraprocessados na obesidade, influenciando políticas públicas e diretrizes nutricionais globalmente.
        
        **DOI:** 10.1016/j.cmet.2019.05.008
        """)
    
    # Artigo 2
    st.markdown("---")
    st.subheader("2. 🍅 Padrões Alimentares Saudáveis e Prevenção de Doenças Crônicas")
    
    with st.expander("📄 Detalhes do Estudo"):
        st.markdown("""
        **Título:** The importance of healthy dietary patterns in chronic disease prevention
        
        **Autor:** Marian L. Neuhouser
        
        **Revista:** Nutrition Research, 2019
        
        **Resumo:** Esta revisão abrangente examina como padrões alimentares saudáveis - ricos em frutas, vegetais, grãos integrais e pobres em gorduras saturadas - reduzem significativamente o risco de diabetes, doenças cardiovasculares e alguns tipos de câncer.
        
        **Importância:** Consolidou décadas de evidências sobre a importância dos padrões alimentares globais versus nutrientes isolados, influenciando as Diretrizes Dietéticas Americanas de 2015-2020.
        
        **DOI:** 10.1016/j.nutres.2018.06.002
        """)
    
    # Artigo 3
    st.markdown("---")
    st.subheader("3. 🫒 Dieta Mediterrânea e Saúde: Uma Visão Abrangente")
    
    with st.expander("📄 Detalhes do Estudo"):
        st.markdown("""
        **Título:** The Mediterranean diet and health: a comprehensive overview
        
        **Autores:** M. Guasch-Ferré, W. C. Willett
        
        **Revista:** Journal of Internal Medicine, 2021
        
        **Resumo:** Esta revisão narrativa fornece evidências robustas dos benefícios da dieta mediterrânea para saúde cardiovascular, controle glicêmico, longevidade e função cognitiva. Também aborda os impactos ambientais positivos deste padrão alimentar.
        
        **Importância:** Consolidou evidências de múltiplos estudos observacionais e de intervenção, estabelecendo a dieta mediterrânea como um dos padrões alimentares mais bem documentados cientificamente.
        
        **DOI:** 10.1111/joim.13333
        """)
    
    # Artigo 4
    st.markdown("---")
    st.subheader("4. 🦠 Influência da Dieta no Microbioma Intestinal e Saúde Humana")
    
    with st.expander("📄 Detalhes do Estudo"):
        st.markdown("""
        **Título:** Influence of diet on the gut microbiome and implications for human health
        
        **Autores:** Rasnik K Singh, Hsin-Wen Chang, Di Yan, et al.
        
        **Revista:** Journal of Translational Medicine, 2017
        
        **Resumo:** Esta revisão sistemática examina como diferentes componentes dietéticos modulam a composição do microbioma intestinal e suas implicações para doenças inflamatórias, obesidade, diabetes tipo 2 e doenças cardiovasculares.
        
        **Importância:** Estabeleceu as bases científicas para compreender a relação dieta-microbioma-saúde, abrindo novos caminhos para intervenções nutricionais personalizadas.
        
        **DOI:** 10.1186/s12967-017-1175-y
        """)
    
    # Artigo 5
    st.markdown("---")
    st.subheader("5. 🌍 Estimativa Global de Inadequações de Micronutrientes")
    
    with st.expander("📄 Detalhes do Estudo"):
        st.markdown("""
        **Título:** Global estimation of dietary micronutrient inadequacies: a modelling analysis
        
        **Autores:** Ty Beal, Christopher D. Gardner, Mario Herrero, et al.
        
        **Revista:** The Lancet Global Health, 2024
        
        **Resumo:** Este estudo de modelagem global revelou que mais de 5 bilhões de pessoas têm ingestão inadequada de iodo, vitamina E e cálcio, enquanto mais de 4 bilhões têm deficiências de ferro, riboflavina, folato e vitamina C.
        
        **Importância:** Forneceu a primeira estimativa global abrangente de inadequações de micronutrientes, informando políticas de saúde pública e programas de fortificação alimentar mundialmente.
        
        **DOI:** 10.1016/S2214-109X(24)00276-6
        """)
    
    # Seção adicional
    st.markdown("---")
    st.subheader("🔬 Por que estes estudos são importantes?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Impacto Científico:**
        - Estudos altamente citados (>100 citações cada)
        - Publicados em revistas de alto impacto
        - Metodologias rigorosas e inovadoras
        - Evidências causais ou correlacionais robustas
        """)
    
    with col2:
        st.markdown("""
        **Relevância Prática:**
        - Influenciam políticas públicas de saúde
        - Orientam diretrizes nutricionais globais
        - Fundamentam práticas clínicas
        - Direcionam pesquisas futuras
        """)
    
    st.markdown("---")
    st.info("""
    💡 **Nota:** Estes artigos representam marcos na ciência da nutrição e continuam influenciando pesquisas, 
    políticas e práticas nutricionais ao redor do mundo. Para aplicações práticas em inferência estatística, 
    muitos destes estudos utilizaram os métodos apresentados nas outras seções deste aplicativo.
    """)

if __name__ == "__main__":
    main()

