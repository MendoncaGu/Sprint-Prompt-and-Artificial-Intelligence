"""
Pipeline de avaliacao - Sprint 04
Le o golden_dataset.json, roda cada caso contra duas versoes do agente
(Groq e Gemini), usa um LLM juiz (Groq) para avaliar cada resposta
contra o criterio_aceite, e calcula a taxa de aprovacao por versao.
"""

import json
import time
import re
from langchain_core.messages import HumanMessage
from main import app_gemini, app_groq, llm
llm_juiz = llm


PROMPT_JUIZ = """Você é um avaliador técnico e imparcial. Avalie se a RESPOSTA abaixo satisfaz o CRITÉRIO DE ACEITE.

CRITÉRIO DE ACEITE:
{criterio}

RESPOSTA A AVALIAR:
{resposta}

Responda EXATAMENTE neste formato, sem texto adicional:
VEREDITO: APROVADO ou REPROVADO
JUSTIFICATIVA: uma frase curta explicando por quê
"""


def rodar_caso_no_agente(app, turnos, thread_id):
    for turno in turnos:
        chamada = app.invoke({"messages": [HumanMessage(turno)]}, config={"configurable": {"thread_id": thread_id}})
    return chamada["messages"][-1].text


def julgar_resposta(criterio, resposta):
    """Manda a resposta para o LLM juiz e extrai veredito + justificativa."""
    prompt = PROMPT_JUIZ.format(criterio=criterio, resposta=resposta)
    saida = llm_juiz.invoke([HumanMessage(prompt)]).text

    veredito_match = re.search(r"VEREDITO:\s*(APROVADO|REPROVADO)", saida, re.IGNORECASE)
    justificativa_match = re.search(r"JUSTIFICATIVA:\s*(.+)", saida, re.IGNORECASE)

    veredito = veredito_match.group(1).upper() if veredito_match else "ERRO_PARSE"
    justificativa = justificativa_match.group(1).strip() if justificativa_match else saida

    return veredito, justificativa


def rodar_pipeline(caminho_dataset):
    with open(caminho_dataset, "r", encoding="utf-8") as f:
        casos = json.load(f)

    versoes = {"groq": app_groq, "gemini": app_gemini}
    resultados = []

    for caso in casos:
        for nome_versao, app_agente in versoes.items():
            thread_id = f"{caso['id']}_{nome_versao}"

            inicio = time.perf_counter()
            resposta = rodar_caso_no_agente(app_agente, caso["turnos"], thread_id)
            latencia = time.perf_counter() - inicio

            veredito, justificativa = julgar_resposta(caso["criterio_aceite"], resposta)

            resultados.append({
                "id": caso["id"],
                "categoria": caso["categoria"],
                "versao": nome_versao,
                "resposta_agente": resposta,
                "latencia_s": round(latencia, 2),
                "veredito": veredito,
                "justificativa_juiz": justificativa,
            })

            print(f"[{caso['id']} | {nome_versao}] -> {veredito} ({latencia:.2f}s) ({justificativa})")

    return resultados


def calcular_taxa_aprovacao(resultados):
    """Calcula % de casos aprovados, por versao."""
    por_versao = {}
    for r in resultados:
        versao = r["versao"]
        por_versao.setdefault(versao, {"aprovados": 0, "total": 0})
        por_versao[versao]["total"] += 1
        if r["veredito"] == "APROVADO":
            por_versao[versao]["aprovados"] += 1

    print("\n" + "=" * 50)
    print("TAXA DE APROVAÇÃO POR VERSÃO")
    print("=" * 50)
    for versao, dados in por_versao.items():
        taxa = 100 * dados["aprovados"] / dados["total"]
        print(f"{versao}: {dados['aprovados']}/{dados['total']} ({taxa:.1f}%)")

    return por_versao


if __name__ == "__main__":
    resultados = rodar_pipeline("golden_dataset.json")

    with open("resultados_avaliacao.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    calcular_taxa_aprovacao(resultados)