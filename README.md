# Template de Chatbot Avançado com Streamlit, Login e Memória Persistente

## 🌟 Visão Geral

Este é um sistema completo de chatbot construído com Streamlit, oferecendo uma experiência profissional com autenticação de usuários, armazenamento persistente de conversas e integração com IA avançada. O sistema é ideal para empresas que desejam implementar um assistente virtual personalizado com capacidade de manter histórico de interações por usuário.

## 🚀 Funcionalidades Principais

### 1. Sistema de Autenticação
- Login seguro através de contas Google
- Autenticação gerenciada pelo Streamlit (`st.user`)
- Proteção de rotas e conteúdo baseado em autenticação
- Registro automático de novos usuários

### 2. Interface de Chat Moderna
- Design responsivo e intuitivo
- Componentes nativos do Streamlit para mensagens
- Indicadores de digitação em tempo real
- Suporte a diferentes tipos de mensagens (texto, links, etc.)

### 3. Sistema de Memória Avançado
- Armazenamento completo do histórico de conversas
- Organização de chats por usuário
- Capacidade de retomar conversas anteriores
- Backup automático das interações

### 4. Gestão de Perfil de Usuário
- Armazenamento de dados básicos:
  * Nome completo
  * Email
  * Foto do perfil
  * Data de cadastro
- Campos personalizáveis:
  * CEP
  * Telefone
  * Data de nascimento
  * Instruções personalizadas para o chatbot

### 5. Sistema de Logs
- Registro detalhado de todas as ações do usuário
- Monitoramento de:
  * Logins/Logouts
  * Criação de novos chats
  * Exclusão de conversas
  * Atualizações de perfil

### 6. Integração com OpenAI
- Utiliza a API mais recente de Assistentes da OpenAI
- Suporte a modelos avançados (GPT-4, GPT-4 Turbo)
- Personalização completa do comportamento do assistente
- Processamento eficiente de prompts

### 7. Painel Administrativo
- Interface protegida por senha
- Visualização de:
  * Lista completa de usuários
  * Histórico de conversas
  * Logs do sistema
  * Métricas de uso

### 8. Documentação Integrada
- Página dedicada com documentação completa
- Guias de uso para usuários
- Instruções de configuração
- Exemplos práticos

### 9. Modo Prova
- Para desativar aulas, corretor AI, professor AI e avaliação AI, altere `MODO_PROVA = True` no app.py

## 🛠️ Configuração do Ambiente

### Requisitos do Sistema
- Python 3.7+
- Conta no Firebase
- Conta na OpenAI
- Ambiente para execução Streamlit

### Passo a Passo de Instalação

1. **Clone o Repositório:**
```bash
git clone <url_do_repositorio>
cd <pasta_do_projeto>
```

2. **Configure o Ambiente Virtual:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Instale as Dependências:**
```bash
pip install -r requirements.txt
```

## 🔧 Configuração das APIs

### Firebase
1. Crie um projeto no Firebase Console
2. Configure o Firestore Database
3. Gere e baixe a chave privada
4. Configure as credenciais no projeto

### OpenAI
1. Crie uma conta na OpenAI
2. Gere uma API Key
3. Configure um Assistente
4. Adicione as credenciais ao projeto

## 📁 Estrutura do Banco de Dados

### Coleção Principal: `chatbot-usuarios`
- Documentos por email do usuário
- Subcoleções:
  * `logs`: Registro de atividades
  * `chats`: Conversas armazenadas

### Estrutura de Dados do Usuário
```json
{
    "email": "string",
    "nome": "string",
    "primeiro_nome": "string",
    "ultimo_nome": "string",
    "foto": "string (URL)",
    "data_cadastro": "timestamp",
    "ultimo_acesso": "timestamp",
    "cep": "string",
    "telefone": "string",
    "instrucoes": "string",
    "data_nascimento": "timestamp"
}
```

## 🚀 Como Executar

1. **Desenvolvimento Local:**
```bash
streamlit run app.py
```

2. **Deploy no Streamlit Cloud:**
- Configure os secrets no painel do Streamlit Cloud
- Conecte com seu repositório
- Deploy automático

## 🎨 Personalização

### Elementos Visuais
- Logos e ícones em `arquivos/`
- Estilos CSS personalizáveis
- Temas do Streamlit configuráveis

### Comportamento do Chatbot
- Instruções personalizáveis via OpenAI
- Configuração de prompts específicos
- Ajuste de parâmetros de resposta

### Campos de Perfil
- Adição/remoção de campos personalizados
- Validações customizadas
- Formatação de dados flexível

## 🔒 Segurança

- Autenticação via Google
- Proteção de rotas administrativas
- Criptografia de dados sensíveis
- Backup automático de dados

## 📚 Arquivos do Projeto

### Estrutura Principal
```
├── app.py                 # Entrada principal
├── requirements.txt       # Dependências
├── .streamlit/
│   └── secrets.toml      # Configurações secretas
├── paginas/
│   ├── chatbot.py        # Interface do chat
│   ├── perfil.py         # Gestão de perfil
│   ├── admin.py          # Painel admin
│   ├── funcoes.py        # Utilitários
│   └── documentacao.py   # Docs do sistema
└── arquivos/             # Recursos estáticos
```

## 🤝 Suporte e Contribuição

- Reporte bugs via Issues
- Sugestões de melhorias são bem-vindas
- Siga as diretrizes de contribuição
- Mantenha o código documentado

## 🤖 Funcionalidades e Usos de Inteligência Artificial

### Visão Geral das Tecnologias de IA Implementadas

O **Stat-AI** é uma plataforma educacional avançada que integra múltiplas tecnologias de Inteligência Artificial para criar uma experiência de aprendizado personalizada e interativa. Abaixo está um relatório completo das funcionalidades e usos de IA implementados:

### 🤖 **Professor AI (Chatbot Inteligente)**
- **Modelo**: OpenAI GPT-4o-mini
- **Técnicas**: RAG (Retrieval Augmented Generation), Engenharia de Prompt
- **Descrição**: Chat conversacional inteligente que acessa automaticamente o conteúdo das aulas para fornecer respostas contextualizadas com referências às fontes, suporte a formatação matemática e histórico persistente.

### ✍️ **Corretor AI (Avaliação de Exercícios)**
- **Modelo**: OpenAI GPT-4o-mini
- **Técnicas**: Engenharia de Prompt
- **Descrição**: Sistema de avaliação construtiva que analisa respostas de exercícios fornecendo feedback personalizado, identificando pontos positivos e áreas de melhoria sem revelar respostas completas.

### 📚 **Gerador de Exercícios AI**
- **Modelo**: OpenAI GPT-4o-mini
- **Técnicas**: Engenharia de Prompt, Streaming API
- **Descrição**: Cria automaticamente 3 exercícios abertos baseados no conteúdo das aulas, incluindo resoluções detalhadas focadas em raciocínio e aplicação prática.

### 💡 **Gerador de Insights AI**
- **Modelo**: OpenAI GPT-4o-mini
- **Técnicas**: Engenharia de Prompt, Streaming API
- **Descrição**: Extrai automaticamente 10 insights principais de cada lição, formatando-os em bullet points concisos com destaque para conceitos importantes.

### ❓ **Quiz AI Interativo**
- **Modelo**: OpenAI GPT-4o-mini
- **Técnicas**: Output Estruturado (JSON Mode)
- **Descrição**: Gera automaticamente quizzes de 5 questões de múltipla escolha com sistema de correção automática, cálculo de pontuação e feedback personalizado.

### 📇 **Flashcards AI**
- **Modelo**: OpenAI GPT-4o-mini
- **Técnicas**: Output Estruturado (JSON Mode)
- **Descrição**: Cria 5-7 flashcards interativos por lição com interface 3D, navegação entre cards e formato frente/verso otimizado para estudo.

### 📝 **Avaliação AI (Prova Simulada)**
- **Modelo**: OpenAI GPT-4o-mini
- **Técnicas**: Output Estruturado (JSON Mode)
- **Descrição**: Gera provas simuladas de 5 questões por módulo com análise completa do conteúdo, questões variadas e métricas de desempenho automáticas.


### 📋 Resumo das Tecnologias de IA Utilizadas

| Tecnologia | Aplicação | Status |
|------------|-----------|--------|
| OpenAI GPT-4o-mini | Chatbot, Avaliação, Geração de Conteúdo | ✅ Implementado |
| RAG (File Search) | Busca semântica em aulas | ✅ Implementado |
| Output Estruturado | Quizzes, Flashcards, Provas | ✅ Implementado |
| Streaming API | Respostas em tempo real | ✅ Implementado |
| Firebase AI | Persistência e Analytics | ✅ Implementado |
| Personalização IA | Adaptação por usuário | ✅ Implementado |
| Analytics IA | Métricas e monitoramento | ✅ Implementado |

### 🎯 Impacto Educacional

O **Stat-AI** representa uma implementação completa de tecnologias de IA para educação, oferecendo:

- **Aprendizado Personalizado**: IA adapta conteúdo e feedback
- **Avaliação Inteligente**: Correção automática com feedback construtivo
- **Geração de Conteúdo**: Criação automática de exercícios e materiais
- **Analytics Avançado**: Monitoramento de progresso e engajamento
- **Experiência Interativa**: Chat, quizzes, flashcards e provas dinâmicas

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. 
