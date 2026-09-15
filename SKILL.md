---
name: fpa-narrative-agent-redesign
description: Use when asked to evaluate, diagnose, or redesign an AI agent that generates executive narratives from monthly financial/FP&A data (variance explanations, contribution-margin bridges, KPI commentary), especially cases that supply driver-level data by segment/business-unit across consecutive periods, a context/memory repository the agent reads, and narratives the agent produced. Also use to build an auditable prototype of such a redesign — deterministic calculation engine, structured evidence contract, falsifiable historical-claims memory, and a narrative checker — with deliverables spanning a written analysis, a Python engine with regression tests, a spreadsheet data source, and an interactive demo page.
---

# Redesenho de agentes de narrativa financeira (FP&A)

## Quando usar
Cases no formato "avalie este agente de IA em produção e proponha o que fazer com ele", em que o agente lê dados consolidados de um período + um repositório de contexto e escreve uma narrativa executiva mensal. Sinais de reconhecimento: dados de driver por unidade/segmento e por período consecutivo; um arquivo de "padrões observados" que cresce sozinho a cada ciclo; pelo menos duas narrativas consecutivas pra comparar uma com a outra.

## Por que esse tipo de case é fácil de errar
O erro mais comum não é aritmético — é de atribuição causal. A narrativa do período mais recente repete o diagnóstico do período anterior porque o repositório de contexto virou uma "regra permanente" em vez de uma hipótese testável a cada rodada. A revisão humana rápida (minutos) checa se o texto soa plausível, não se ele reconcilia com a planilha — e deixa passar. A lista completa do que evitar está em `references/checklist-redesenho.md`.

## Fluxo de trabalho

1. **Nunca confie na prosa.** Recalcule o KPI (margem, receita, o que for) por unidade e por período a partir dos drivers brutos. Se o case dá um total de referência, seu recálculo TEM que reconciliar com ele antes de qualquer leitura qualitativa — é a prova de que a fórmula usada está certa, não uma formalidade.

2. **Avalie cada narrativa contra o recálculo**, de preferência frase por frase, apontando exatamente qual afirmação bate e qual não bate — com números, não com adjetivos.

3. **Diagnostique a causa raiz olhando o pipeline, não só o texto**: onde cálculo e narração se misturam num único passo sem artefato intermediário auditável; onde o repositório trata um padrão observado como regra permanente; o que a revisão humana consegue checar no tempo que tem (normalmente não dá pra recalcular nada nesse tempo — só ler se soa coerente).

4. **Redesenhe com 2 a 3 decisões, nunca dez.** As duas que praticamente sempre se aplicam:
   - **Calcular antes de narrar**: um contrato de evidência estruturado (números por unidade, driver principal, flag de reconciliação) é gerado *antes* de qualquer texto; a narrativa vira função dessa evidência, nunca o contrário. O LLM nunca escolhe sozinho o driver principal.
   - **Memória como claims falsificáveis**: cada padrão histórico vira `{driver, direção esperada, status}`, testado contra a evidência do período atual a cada rodada — nunca uma regra permanente que se autorreforça.

5. **Prove com teste, não com intenção.** Monte pelo menos três casos:
   - **Caso A** — o padrão histórico se confirma (normalmente o primeiro dos dois períodos do case).
   - **Caso B** — o padrão quebra (normalmente o período mais recente — o erro real que motivou o case). É o teste mais importante: se o redesenho ainda repetir o diagnóstico antigo aqui, ele falhou.
   - **Caso C** — evidência ambígua/insuficiente, cenário **sintético** e claramente rotulado como tal (não invente dado real).
   Rode um checker com `assert` contra os três — aprovação humana subjetiva não é suficiente.

6. **Monte os entregáveis a partir dos templates**, não do zero:
   - Documento de avaliação (.md) → `templates/analise-template.md`
   - Motor determinístico em Python + os 3 casos de teste → `templates/agent_engine_template.py` (troque os nomes das unidades de negócio e a fórmula do KPI na seção `AJUSTE AQUI` do topo do arquivo)
   - Fonte de dados em planilha, não embutida no código (mais realista e mais fácil de auditar) → `templates/build_excel_template.py`
   - Landing page interativa (Agent Run, Evidence, Narrative, Validation, Methodology, Concepts) → `examples/landing_reference.html` é um **exemplo trabalhado** (case Vértice, identidade visual Creditas), não um template genérico: copie e adapte os nomes de unidade, os dados e os tokens de cor no topo do CSS/JS.

## Entregável mínimo mesmo sob prazo apertado
Se não der tempo para o protótipo interativo completo, a ordem de prioridade (a mesma que os cases desse tipo cobram na avaliação) é: **1) diagnóstico numérico correto e reconciliado > 2) causa raiz bem defendida > 3) redesenho com teste que roda (mesmo que só o script Python) > 4) riscos honestos > 5) protótipo visual.** Um script que roda e prova o ponto vale mais que uma landing page bonita sobre um diagnóstico furado.

## Referências
- `references/checklist-redesenho.md` — lista condensada do que nunca fazer nesse tipo de redesenho, e os critérios de avaliação típicos do case.
- `docs-originais/` — os dois documentos-fonte completos que geraram esta skill (especificação do Agent Run/landing page e os princípios de redesenho), preservados na íntegra por rastreabilidade.
- `processo-sessao/` — recapitulação cronológica de toda a sessão que gerou esta skill, a lista das skills do Claude efetivamente usadas, e os `.json` reais (não fabricados) dos contratos de evidência e resultados do checker para os 3 casos de teste.
