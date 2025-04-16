import streamlit as st
from paginas.funcoes import registrar_atividade_academica

# Título da página
st.title("Guided Learning Experience")
st.markdown("#### O Futuro da Educação Está Sendo Construído! 🔮")

col1, col2 = st.columns([1,3])

with col1:
    # Imagem de construção
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjI1cXlnY2swMmRmcW92cW95bWp3bWpmZWJ3NHZmODZ1ZWd2aHhhYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JIX9t2j0ZTN9S/giphy.gif", width=300)

with col2:
    # Texto principal com tom divertido
    st.markdown("""
   
    
    ### O que vem por aí:

    * 🤖 IA personalizada que entende seu estilo de aprendizado 
    * 🎮 Gamificação que vai fazer você esquecer que está estudando
    * 🔄 Ciclos de feedback instantâneos (porque esperar é tããão século XX)

    ### Status atual: 

    ```
    Programador: "Só mais um coquinha zero e termino isso..."  
    ```


    """)

 
# Registra atividade se implementado no sistema
try:
    registrar_atividade_academica(
        tipo="exploracao",
        modulo="Guided Learning",
        detalhes={
            "acao": "visita_pagina",
            "pagina": "Guided Learning Experience"
        }
    )
except:
    pass  # Se a função não estiver implementada corretamente, ignora 