import streamlit as st
from openai import OpenAI
import json

# Modelo padrão para as funções auxiliares (pode ser ajustado ou passado como argumento)
MODELO_PADRAO = 'gpt-4o-mini'

# Helper para obter cliente OpenAI (evita repetição e centraliza erro de chave)
def _get_openai_client():
    """Retorna um cliente OpenAI inicializado ou None se a chave não for encontrada."""
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        return OpenAI(api_key=api_key)
    except KeyError:
        st.error("Erro de configuração: Chave secreta 'OPENAI_API_KEY' não encontrada.")
        return None
    except Exception as e:
        st.error(f"Erro ao inicializar cliente OpenAI: {e}")
        return None

# --- Funções para Geração de Conteúdo (Aulas) ---

def gerar_exercicios_licao(conteudo_licao: str):
    """Chama a IA para gerar exercícios baseados no conteúdo da lição."""
    client = _get_openai_client()
    if not client:
        return None # Retorna None se cliente falhar

    prompt = f"""
Você é um assistente de professor cuja tarefa é escrever uma lista de exercícios baseada no <material de aula> abaixo.
- Sua tarefa é criar apenas 3 exercícios abertos.
- Cada exercício deve conter uma pergunta aberta clara e bem elaborada.
- O objetivo é estimular raciocínio, argumentação ou aplicação prática do conteúdo.
- O output deve conter apenas os 3 exercícios abertos, seguidos de uma breve resolução para cada um, separada por sessão.
- Use formatação, como negrito e itálico quando necessário.
- Use emojis apenas quando forem pertinentes.
- O output deve conter somente os exercícios e resoluções, sem introduções, explicações ou comentários extras.
    
    <material de aula>
    {conteudo_licao}
    </material de aula>
    """
    try:
        # Usamos stream=True aqui porque o original usava
        stream = client.chat.completions.create(
            model=MODELO_PADRAO,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Erro ao gerar exercícios: {e}")
        return None

def gerar_insights_licao(conteudo_licao: str):
    """Chama a IA para gerar insights baseados no conteúdo da lição."""
    client = _get_openai_client()
    if not client:
        return None

    prompt = f"""Você é um assistente que tem a função de utilizar um <material de aula> e processar seguindo as seguintes instruções:
    - Leia e compreenda integralmente o material de aula para captar o contexto, os tópicos abordados e a progressão dos conceitos.
    - Escreva um output que seja uma coleção de 10 insights sobre a aula.
    - Use bullet points para cada insight. 
    - use texto normal nos titulos das sessões. 
    - cada insight deve ter no máximo 140 caracteres.
    - seu output deve ser apenas, e somente apenas, a lista de insights.
    - use negrito e italico para destacar o que for importante.

    O material da aula é o seguinte:

    <material de aula>
    {conteudo_licao}
    </material de aula>
    """
    try:
        # Usamos stream=True aqui porque o original usava
        stream = client.chat.completions.create(
            model=MODELO_PADRAO,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Erro ao gerar insights: {e}")
        return None

def gerar_quiz_licao(conteudo_licao: str):
    """Chama a IA para gerar um quiz em formato JSON."""
    client = _get_openai_client()
    if not client:
        return None

    # Escapa chaves no conteúdo da lição para evitar erros na f-string
    conteudo_licao_escaped = conteudo_licao.replace('{', '{{').replace('}', '}}')

    prompt_quiz = f"""
    Você é um assistente educacional especialista em criar quizzes em formato JSON.
    Baseado no <material de aula> abaixo, crie um quiz contendo EXATAMENTE:
    - 5 perguntas de múltipla escolha (com 4 alternativas cada).
    
    **Formato de Saída OBRIGATÓRIO:** JSON com chaves "perguntas" (lista de dicts com "numero" (int ou str), "tipo", "enunciado", "opcoes") e "gabarito" (um dicionário onde cada chave é o NÚMERO DA PERGUNTA COMO STRING e o valor é a alternativa correta como string). Exemplo de gabarito: {{"1": "Opção A", "2": "Opção C"}}.
    NÃO inclua nenhuma explicação ou texto fora do objeto JSON.

    <material de aula>
    {conteudo_licao_escaped}
    </material de aula>
    """ # Instruções detalhadas do JSON omitidas aqui por brevidade (assumindo que o prompt completo está correto)
    
    try:
        completion = client.chat.completions.create(
            model=MODELO_PADRAO,
            messages=[{"role": "user", "content": prompt_quiz}],
            response_format={ "type": "json_object" }
        )
        resposta_json_str = completion.choices[0].message.content
        
        try:
            quiz_data = json.loads(resposta_json_str)
            if "perguntas" in quiz_data and "gabarito" in quiz_data:
                return quiz_data # Retorna o dicionário parseado
            else:
                st.error("A IA retornou um JSON em formato inesperado (sem chaves 'perguntas' ou 'gabarito').")
                print("Erro: JSON sem chaves esperadas", quiz_data)
                return None
        except json.JSONDecodeError as json_err:
            st.error("Erro ao processar a resposta da IA (não é um JSON válido). Tente gerar novamente.")
            print("Erro de JSON Decode:", json_err)
            print("String recebida:", resposta_json_str)
            return None
            
    except Exception as e:
        st.error(f"Erro ao gerar quiz: {e}")    
        return None

def gerar_flashcards_licao(conteudo_licao: str):
    """Chama a IA para gerar flashcards em formato JSON."""
    client = _get_openai_client()
    if not client:
        return None

    prompt_flashcards = f"""
    Você é um assistente educacional especialista em criar flashcards em formato JSON.
    Baseado no <material de aula> abaixo, crie uma lista de 5 a 7 flashcards.
    
    **Formato de Saída OBRIGATÓRIO:** JSON com chave "flashcards" (lista de dicts com "frente" e "verso").
    NÃO inclua nenhuma explicação ou texto fora do objeto JSON.

    <material de aula>
    {conteudo_licao}
    </material de aula>
    """ # Instruções detalhadas do JSON omitidas por brevidade
    
    try:
        completion = client.chat.completions.create(
            model=MODELO_PADRAO,
            messages=[{"role": "user", "content": prompt_flashcards}],
            response_format={ "type": "json_object" }
        )
        resposta_json_str = completion.choices[0].message.content
        
        try:
            flashcard_data = json.loads(resposta_json_str)
            if "flashcards" in flashcard_data and isinstance(flashcard_data["flashcards"], list):
                 # Retorna a lista de flashcards ou None se estiver vazia
                 return flashcard_data["flashcards"] if flashcard_data["flashcards"] else None
            else:
                st.error("A IA retornou um JSON em formato inesperado (sem chave 'flashcards' ou não é lista).")
                print("Erro: JSON sem chave 'flashcards' ou não é lista", flashcard_data)
                return None
        except json.JSONDecodeError as json_err:
            st.error("Erro ao processar a resposta da IA (não é um JSON válido). Tente gerar novamente.")
            print("Erro de JSON Decode:", json_err)
            print("String recebida:", resposta_json_str)
            return None
            
    except Exception as e:
        st.error(f"Erro ao gerar flashcards: {e}")
        return None

# --- Função para Avaliação (Exercícios) ---

def avaliar_resposta_exercicio(enunciado_exercicio: str, resposta_aluno: str):
    """Chama a IA para avaliar a resposta de um aluno a um exercício."""
    client = _get_openai_client()
    if not client:
        return None # Retorna None se cliente falhar

    prompt = f"""
    Você é um **tutor amigável e encorajador**, especialista em ajudar alunos a entenderem estatística. Seu objetivo é fornecer feedback construtivo e motivador.
    
    **Exercício Selecionado:**
    <enunciado do exercício>
    {enunciado_exercicio}
    </enunciado do exercício>
    
    **Tarefa:** Avalie a <resposta do aluno> fornecida para o <enunciado do exercício> de forma clara e gentil.
    
    **Instruções para Avaliação:**
    1.  **Avaliação Geral:** Comece indicando se a resposta está no caminho certo, se precisa de alguns ajustes ou se há equívocos importantes. Use uma linguagem positiva e de apoio.
    2.  **Pontos Positivos:** Se houver acertos parciais ou um bom começo, destaque isso primeiro! (ex: "Você começou muito bem ao identificar...", "Seu raciocínio sobre X está correto!").
    3.  **Áreas para Melhoria (Se Incorreta ou Parcialmente Correta):**
        a. Explique o(s) principal(is) erro(s) conceitual(is) ou de cálculo de forma clara e paciente. Evite linguagem que possa desmotivar.
        b. **Ofereça dicas construtivas** sobre o que o aluno pode revisar ou como pode repensar a questão (ex: "Que tal revisar o conceito de...?", "Uma dica: a fórmula para Y pode ser útil aqui.", "Tente pensar se há outros fatores que influenciam Z.").
        c. **NÃO** forneça a resposta correta completa, mas você pode guiar o aluno para que ele mesmo a encontre.
    4.  **Tom:** Mantenha um tom positivo, paciente e encorajador durante toda a avaliação.
    5.  Use markdown para formatação básica (negrito, itálico) para melhorar a legibilidade.
    
    **Resposta do Aluno:**
    <resposta do aluno>
    {resposta_aluno}
    </resposta do aluno>
    
    **Sua Avaliação Encorajadora:**
    """
    try:
        completion = client.chat.completions.create(
            model=MODELO_PADRAO, # Usar 'gpt-4o-mini' ou talvez 'gpt-4' para melhor avaliação
            messages=[{"role": "user", "content": prompt}]
            # stream=False implícito
        )
        response_content = completion.choices[0].message.content
        return response_content
    except Exception as e:
        st.error(f"Erro ao avaliar resposta: {e}")
        return None

# --- Função para Geração de Título (Chatbot) ---

def gerar_titulo_chat(primeiro_prompt: str):
    """Chama a IA para gerar um título curto para um chat."""
    client = _get_openai_client()
    if not client:
        return None # Retorna None se cliente falhar

    try:
        response_titulo = client.chat.completions.create(
            model=MODELO_PADRAO,  # Modelo mais rápido é suficiente para títulos
            messages=[
                {"role": "system", "content": "Você é um assistente que cria títulos curtos (máximo 5 palavras) para conversas de chat, baseado no primeiro prompt do usuário."},
                {"role": "user", "content": f"Crie um título curto para uma conversa que começa com: '{primeiro_prompt}'"}
            ],
            temperature=0.5,
            max_tokens=20 # Limita o tamanho do título
        )
        titulo_sugerido = response_titulo.choices[0].message.content.strip().replace('"' ,'')
        return titulo_sugerido
    except Exception as e:
        print(f"Erro ao gerar título do chat com LLM: {e}")
        # Fallback pode ser tratado fora desta função ou retornar None
        return None 

# --- Função para Geração de Prova Simulado (Prova AI) ---

def gerar_prova_simulada(conteudo_modulo: str, nomes_licoes: list[str]):
    """Chama a IA para gerar uma prova simulada (quiz) de 5 questões em JSON.
    
    Args:
        conteudo_modulo: String contendo o conteúdo concatenado das lições do módulo.
        nomes_licoes: Lista com os nomes das lições incluídas.
        
    Returns:
        dict: Dicionário com as chaves 'perguntas' e 'gabarito' ou None em caso de erro.
    """
    client = _get_openai_client()
    if not client:
        return None

    prompt_prova = f"""
    Você é um assistente especialista em criar provas simuladas em formato JSON.
    O objetivo é avaliar a compreensão do aluno sobre um módulo de estatística, cujo conteúdo é fornecido abaixo, extraído das seguintes lições: {', '.join(nomes_licoes)}. 
    
    Crie uma prova contendo EXATAMENTE 5 questões variadas (conceituais, cálculo simples, interpretação) sobre os tópicos principais abordados no material.
    
    **Formato de Saída OBRIGATÓRIO:** JSON com chaves "perguntas" (lista de 5 dicts com numero, tipo="multipla_escolha", enunciado, opcoes=[4 strings]) e "gabarito" (dict numero_str:resposta_correta_str).
    NÃO inclua nenhuma explicação ou texto fora do objeto JSON.
    
    <conteudo_modulo>
    {conteudo_modulo}
    </conteudo_modulo>
    """ # Detalhes do formato JSON omitidos por brevidade

    try:
        completion = client.chat.completions.create(
            model='gpt-4o-mini', # Considerar modelo mais potente se necessário
            messages=[{"role": "user", "content": prompt_prova}],
            response_format={ "type": "json_object" }
        )
        resposta_json_str = completion.choices[0].message.content
        try:
            prova_data = json.loads(resposta_json_str)
            # Validação mais robusta
            if (
                "perguntas" in prova_data and 
                "gabarito" in prova_data and 
                isinstance(prova_data["perguntas"], list) and 
                len(prova_data["perguntas"]) == 5 and
                isinstance(prova_data["gabarito"], dict) and
                len(prova_data["gabarito"]) == 5
               ):
                # Verifica estrutura interna (opcional, mas recomendado)
                is_structure_ok = True
                for p in prova_data["perguntas"]:
                    if not all(k in p for k in ["numero", "tipo", "enunciado", "opcoes"]) or len(p["opcoes"]) != 4:
                        is_structure_ok = False
                        break
                if is_structure_ok and set(prova_data["gabarito"].keys()) == set(str(i) for i in range(1, 6)):
                     return prova_data
                else:
                     st.error("A IA retornou um JSON com estrutura interna inválida nas perguntas ou gabarito.")
                     print("Erro: Estrutura interna JSON inválida", prova_data)
                     return None
            else:
                st.error("A IA retornou um JSON em formato ou tamanho inesperado. Tente gerar novamente.")
                print("Erro: JSON inválido ou incompleto", prova_data)
                return None
        except json.JSONDecodeError as json_err:
            st.error("Erro ao processar a resposta da IA (não é um JSON válido). Tente gerar novamente.")
            print("Erro de JSON Decode:", json_err)
            print("String recebida:", resposta_json_str)
            return None
    except Exception as e:
        st.error(f"Erro ao gerar prova via IA: {e}")
        return None 