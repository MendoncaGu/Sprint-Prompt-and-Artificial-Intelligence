# GoodWe Charge Assistant — Sprint 03

Chatbot conversacional para suporte a carregadores elétricos e eletropostos GoodWe, desenvolvido para o EV Challenge — GoodWe. Nesta sprint, o núcleo conversacional foi refatorado para utilizar um framework de agentes de IA, incorporando memória de sessão, guardrails de segurança e comparação entre modelos de linguagem.

## Framework escolhido

**LangGraph**, parte do ecossistema LangChain.

**Motivo da escolha:** o projeto já tinha familiaridade prévia com LangChain nas sprints anteriores. O LangGraph foi escolhido especificamente por oferecer gerenciamento de estado e memória de sessão nativos (via `checkpointer`), resolvendo diretamente o requisito de memória por sessão da sprint sem a necessidade de implementar controle de histórico manualmente.

**Principais componentes utilizados:**
- `StateGraph` + `MessagesState` — orquestração do fluxo conversacional
- `MemorySaver` — checkpointer para persistência de memória por sessão (`thread_id`)
- `SystemMessage` — guardrail de comportamento e escopo do agente
- `init_chat_model` — abstração de modelo, permitindo alternar entre provedores (Groq/Gemini) sem alterar a lógica do agente

**Vantagens encontradas:**
- Troca de modelo de linguagem exige alteração de apenas uma linha de código
- Memória de sessão funcional sem implementação manual de histórico
- Separação clara entre orquestração (grafo) e lógica de geração (nó do agente)

**Limitações/trade-offs identificados:**
- `MemorySaver` armazena o histórico apenas em memória RAM do processo (não persiste entre execuções do programa)
- System prompt, isoladamente, reduz mas não elimina alucinação técnica do modelo
- Camadas gratuitas dos provedores de LLM têm cotas restritivas (ver `relatorio_modelos.md`)

## Como rodar o projeto

### 1. Pré-requisitos
- Python 3.9 ou superior

### 2. Configuração do ambiente

```bash
python -m venv venv
```

Ativar o ambiente virtual:
- Windows: `.\venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (use `.env.example` como referência) com:

```
GROQ_API_KEY=sua_chave_groq
GOOGLE_API_KEY=sua_chave_gemini
```

- Chave Groq: [console.groq.com](https://console.groq.com)
- Chave Gemini: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 5. Executar

```bash
python main.py
```

## Estrutura do repositório

```
├── main.py                 # Núcleo do agente (grafo, memória, guardrails, testes)
├── requirements.txt         # Dependências do projeto
├── .env.example             # Modelo de variáveis de ambiente necessárias
├── .gitignore
├── relatorio_modelos.md     # Comparação entre Groq e Gemini (Bloco B)
└── README.md
```

## Entregáveis da Sprint 03

- **Código-fonte:** `main.py`
- **Comparação de modelos:** [`relatorio_modelos.md`](./relatorio_modelos.md)
- **Testes de memória e segurança:** documentados nos logs de execução e no `relatorio_modelos.md`
- **Relatório de evolução (PDF):** *(a ser adicionado)*
- **Identificação da equipe:** *(arquivo `.txt` a ser adicionado)*

## Equipe

*(nome, RM e responsabilidade de cada integrante — a preencher)*
