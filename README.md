# Template de Chatbot Avançado com Streamlit, Login e Memória Persistente

## 🌟 Visão Geral

Este é um sistema completo de chatbot construído com Streamlit, oferecendo uma experiência profissional com autenticação de usuários, armazenamento persistente de conversas e integração com IA avançada. O sistema é ideal para empresas que desejam implementar um assistente virtual personalizado com capacidade de manter histórico de interações por usuário.

## 🚀 Funcionalidades Principais

### 1. Sistema de Autenticação
- Login seguro através de contas Google
- Autenticação gerenciada pelo Streamlit (`st.experimental_user`)
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

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. 