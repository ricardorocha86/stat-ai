import streamlit as st
from paginas.funcoes import registrar_atividade_academica

# Título da página
st.title("🚀 Guided Learning Experience")

 
# Imagem de construção
st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjI1cXlnY2swMmRmcW92cW95bWp3bWpmZWJ3NHZmODZ1ZWd2aHhhYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JIX9t2j0ZTN9S/giphy.gif", width=300)

# Texto principal com tom divertido
st.markdown("""
## 🔮 O Futuro da Educação Está Sendo Construído
 
### O que vem por aí:

* 🤖 IA personalizada que entende seu estilo de aprendizado 
* 🎮 Gamificação que vai fazer você esquecer que está estudando
* 🔄 Ciclos de feedback instantâneos (porque esperar é tããão século XX)

### Status atual: 

```
Programador: "Só mais um coquinha zero e termino isso..." 
```

### Volte em breve!

Enquanto isso, continue aproveitando nossos recursos atuais. A revolução está sendo codificada, testada, recodificada, chorada em cima, consertada com fita adesiva, e finalmente... transformada em algo incrível!
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