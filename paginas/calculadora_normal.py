import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
from scipy.stats import norm, t, chi2
import seaborn as sns

# Configuração da página
st.set_page_config(
    page_title="Calculadora da Normal",
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
    st.title("📊 Calculadora da Normal")
    st.markdown("---") 

    # Layout de duas colunas principais
    col_controles, col_grafico = st.columns([1, 2])
    
    with col_controles:
        st.subheader("⚙️ Controles")
        
        # Seleção do tipo de cálculo
        tipo_calculo_geral = st.radio(
            "Selecione o que deseja calcular:",
            ("Probabilidades", "Intervalo de Confiança"),
            key="tipo_calculo_geral"
        )
        st.markdown("---")

        # Inputs básicos
        st.write("**Parâmetros da Distribuição:**")
        media = st.number_input("Média (μ):", value=0.0, step=0.1)
        desvio_padrao = st.number_input("Desvio padrão (σ):", value=1.0, step=0.1, min_value=0.1)
        
        st.markdown("---")
        
        # Inputs específicos para cada tipo de cálculo
        if tipo_calculo_geral == "Probabilidades":
            st.write("**Configurações de Probabilidade:**")
            tipo_calculo_prob = st.selectbox("Tipo de cálculo:", 
                                       ["P(X < x)", "P(X > x)", "P(a < X < b)"])
            
            if tipo_calculo_prob in ["P(X < x)", "P(X > x)"]:
                valor_x = st.number_input("Valor x:", value=0.0, step=0.1)
            else:
                valor_a = st.number_input("Valor a:", value=-1.0, step=0.1)
                valor_b = st.number_input("Valor b:", value=1.0, step=0.1)
        else: # Intervalo de Confiança
            st.write("**Configurações do Intervalo:**")
            nivel_confianca = st.number_input("Nível de confiança (%):", min_value=1.0, max_value=99.9, value=95.0, step=0.5)

        st.markdown("---")
        # Botão de cálculo
        calcular = st.button("🔢 Calcular", use_container_width=True, type="primary")

    with col_grafico:
        st.subheader("📈 Visualização")
        
        # Cálculos
        if calcular:
            if "tipo_calculo_geral" in st.session_state:
                del st.session_state["tipo_calculo_geral"]
            configurar_grafico()
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Gerar dados para a curva
            x = np.linspace(media - 4*desvio_padrao, media + 4*desvio_padrao, 1000)
            y = norm.pdf(x, media, desvio_padrao)
            
            # Plotar a curva normal
            ax.plot(x, y, 'b-', linewidth=2, label='Distribuição Normal')
            
            if tipo_calculo_geral == "Probabilidades":
                # Calcular probabilidade e área sombreada
                if tipo_calculo_prob == "P(X < x)":
                    probabilidade = norm.cdf(valor_x, media, desvio_padrao)
                    valor_z = (valor_x - media) / desvio_padrao
                    
                    # Área sombreada
                    x_fill = x[x <= valor_x]
                    y_fill = norm.pdf(x_fill, media, desvio_padrao)
                    ax.fill_between(x_fill, y_fill, alpha=0.3, color='red', label=f'P(X < {valor_x})')
                    
                    # Linha vertical
                    ax.axvline(valor_x, color='red', linestyle='--', linewidth=2)
                    ax.annotate(f'x = {valor_x}', xy=(valor_x, 0), xytext=(valor_x, 0.05 * y.max()),
                               arrowprops=dict(arrowstyle='->', color='red'))
                    
                    resultado_texto = f"A probabilidade de X ser menor que {valor_x} é {probabilidade:.4f}"
                    titulo_grafico = f'Distribuição Normal (μ={media}, σ={desvio_padrao})'

                elif tipo_calculo_prob == "P(X > x)":
                    probabilidade = 1 - norm.cdf(valor_x, media, desvio_padrao)
                    valor_z = (valor_x - media) / desvio_padrao
                    
                    # Área sombreada
                    x_fill = x[x >= valor_x]
                    y_fill = norm.pdf(x_fill, media, desvio_padrao)
                    ax.fill_between(x_fill, y_fill, alpha=0.3, color='green', label=f'P(X > {valor_x})')
                    
                    # Linha vertical
                    ax.axvline(valor_x, color='green', linestyle='--', linewidth=2)
                    ax.annotate(f'x = {valor_x}', xy=(valor_x, 0), xytext=(valor_x, 0.05 * y.max()),
                               arrowprops=dict(arrowstyle='->', color='green'))
                    
                    resultado_texto = f"A probabilidade de X ser maior que {valor_x} é {probabilidade:.4f}"
                    titulo_grafico = f'Distribuição Normal (μ={media}, σ={desvio_padrao})'

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
                    ax.annotate(f'a = {valor_a}', xy=(valor_a, 0), xytext=(valor_a, 0.05 * y.max()),
                               arrowprops=dict(arrowstyle='->', color='blue'))
                    ax.annotate(f'b = {valor_b}', xy=(valor_b, 0), xytext=(valor_b, 0.05 * y.max()),
                               arrowprops=dict(arrowstyle='->', color='blue'))
                    
                    resultado_texto = f"A probabilidade de X estar entre {valor_a} e {valor_b} é {probabilidade:.4f}"
                    titulo_grafico = f'Distribuição Normal (μ={media}, σ={desvio_padrao})'

            else: # Intervalo de Confiança
                confianca = nivel_confianca / 100.0
                alpha = 1 - confianca

                limite_inferior = norm.ppf(alpha / 2, loc=media, scale=desvio_padrao)
                limite_superior = norm.ppf(1 - alpha / 2, loc=media, scale=desvio_padrao)
                
                # Área sombreada
                x_fill = x[(x >= limite_inferior) & (x <= limite_superior)]
                y_fill = norm.pdf(x_fill, media, desvio_padrao)
                ax.fill_between(x_fill, y_fill, alpha=0.3, color='purple', label=f'Intervalo de {nivel_confianca}%')
                
                # Linhas verticais
                ax.axvline(limite_inferior, color='purple', linestyle='--', linewidth=2)
                ax.axvline(limite_superior, color='purple', linestyle='--', linewidth=2)
                ax.annotate(f'LI = {limite_inferior:.4f}', xy=(limite_inferior, 0), xytext=(limite_inferior, 0.05 * y.max()),
                           arrowprops=dict(arrowstyle='->', color='purple'), ha='center')
                ax.annotate(f'LS = {limite_superior:.4f}', xy=(limite_superior, 0), xytext=(limite_superior, 0.05 * y.max()),
                           arrowprops=dict(arrowstyle='->', color='purple'), ha='center')
                
                resultado_texto = f"O intervalo que contém {nivel_confianca}% da probabilidade é [{limite_inferior:.4f}, {limite_superior:.4f}]"
                titulo_grafico = f'Intervalo de Confiança de {nivel_confianca}% (μ={media}, σ={desvio_padrao})'
            
            ax.set_xlabel('Valores de X')
            ax.set_ylabel('Densidade de Probabilidade')
            ax.set_title(titulo_grafico)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
            # Resultados
            st.success(f"**Resultado:** {resultado_texto}")
            if tipo_calculo_geral == "Probabilidades":
                if tipo_calculo_prob != "P(a < X < b)":
                    st.info(f"**Valor Z correspondente:** {valor_z:.4f}")
        else:
            # Mostrar placeholder quando não há cálculo
            st.info("👈 Configure os parâmetros na coluna da esquerda e clique em 'Calcular' para visualizar o gráfico.")

if __name__ == "__main__":
    main()

