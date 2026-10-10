# GoodWe Charge Assistant — Sprint 04

Agente conversacional de suporte a carregadores elétricos e eletropostos GoodWe, desenvolvido para o EV Challenge — GoodWe.

Nas sprints anteriores o agente foi planejado (Sprint 1), implementado (Sprint 2) e reconstruído com LangGraph, memória por sessão e guardrails (Sprint 3). A Sprint 04 substitui a avaliação manual da Sprint 3 por um **pipeline de avaliação automatizado**, que roda um golden dataset contra duas versões do agente e usa um LLM como juiz.

## Resultado principal

| Métrica | Groq | Gemini |
|---|---|---|
| Taxa de aprovação (juiz) | 10/11 (90,9%) | 10/11 (90,9%) |
| Taxa de aprovação (revisão manual) | 9/11 (81,8%) | 10/11 (90,9%) |
| Latência mediana | 0,95 s | 7,05 s |

Versão escolhida: **Groq**, por qualidade equivalente e latência cerca de 7 vezes menor. A análise completa está no relatório final.

## Arquitetura

- **Agente (`main.py`)**: dois grafos LangGraph (`app_groq` e `app_gemini`), cada um com `MemorySaver` para memória por `thread_id` e o mesmo system prompt de guardrail.
- **Golden dataset (`golden_dataset.json`)**: 11 casos com turnos e critério de aceite, cobrindo memória, Prompt Injection, alucinação técnica, escopo, aconselhamento jurídico e financeiro, segurança elétrica e caso de borda.
- **Pipeline (`pipeline_avaliacao.py`)**: importa os agentes reais, roda cada caso em cada versão, mede a latência, envia a resposta ao juiz (modelo Groq puro, sem guardrail) e calcula a taxa de aprovação por versão.

## Como rodar

Todos os comandos abaixo rodam de dentro da pasta `sprint-04`.

### 1. Ambiente

```bash
python -m venv venv
```

Ativar:
- Windows: `.\venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

```bash
pip install -r requirements.txt
```

### 2. Chaves de API

Crie um arquivo `.env` na raiz (use o `.env.example` como modelo):

```
GROQ_API_KEY=sua_chave_groq
GOOGLE_API_KEY=sua_chave_gemini
```

- Groq: [console.groq.com](https://console.groq.com)
- Gemini: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 3. Executar

Testes manuais da Sprint 3 (memória e Prompt Injection nas duas versões):

```bash
python main.py
```

Pipeline de avaliação da Sprint 04:

```bash
python pipeline_avaliacao.py
```

O pipeline salva os resultados em `resultados_avaliacao.json` e imprime a taxa de aprovação de cada versão.

**Atenção à cota:** a camada gratuita do Gemini permite 20 chamadas por dia. Uma rodada completa do pipeline usa 14, e o `main.py` usa mais 5. Rodar os dois no mesmo dia estoura a cota.

## Estrutura do repositório

```
├── main.py                         # Agentes Groq e Gemini (LangGraph + memória + guardrail)
├── pipeline_avaliacao.py           # Pipeline de avaliação com LLM as a judge
├── golden_dataset.json             # 11 casos de teste com critério de aceite
├── resultados_rodada1.json         # Rodada 1: 4 casos, juiz Gemini
├── resultados_teste_groq.json      # Teste: 11 casos, só Groq, juiz Groq
├── resultados_rodada_final.json    # Rodada final: 11 casos, Groq e Gemini, juiz Groq
├── relatorio_final_sprint04.pdf    # Relatório final da Sprint 04
├── identificacao_equipe.txt        # Nome, RM e turma dos integrantes
├── requirements.txt
├── .env.example
└── README.md
```

## Limitações conhecidas

- O juiz pode ser inconsistente em casos de fronteira e, na rodada final, julga as respostas do próprio modelo.
- O juiz não tem fonte da verdade sobre o catálogo GoodWe: ele não confirma se um produto citado existe.
- Cada versão foi avaliada em uma única rodada, e os modelos não são determinísticos.
- Com 11 casos, um único caso vale cerca de 9 pontos percentuais.

## Equipe — Turma 1 CCPX

| Nome | RM |
|---|---|
| Ângelo Malta Reina | 570769 |
| Gustavo Mendonça Duarte | 570561 |
| Matheus Carpinheiro Moreno | 571770 |
| Renan de Castro Albuquerque | 570532 |
| Vinícius Souza Ferraz | 570622 |
