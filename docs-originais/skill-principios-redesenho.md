# Agente FP&A Vértice — O agente que conta a história dos números

*Segundo documento-fonte colado no chat durante a construção desta skill — os
princípios de redesenho, a lista extensa do que não fazer, o contrato entre
camadas e a definição de "pronto". Preservado na íntegra por rastreabilidade;
`references/checklist-redesenho.md` é a versão condensada que o `SKILL.md`
usa no dia a dia.*

## Propósito

Construir, avaliar e demonstrar um agente de IA para FP&A capaz de transformar dados financeiros em uma narrativa executiva correta, verificável e orientada à decisão — evolução do agente existente no case da Vértice, não um projeto genérico de dashboard, chatbot ou automação de BI.

## 1. Regra de ouro

Não otimizar para uma narrativa convincente. Otimizar para uma narrativa **falsificável**. Uma narrativa bonita, fluida e coerente com o histórico não é evidência de qualidade. O agente só deve afirmar uma causa quando existir evidência quantitativa suficiente para sustentá-la.

Cadeia esperada: `DADOS → CÁLCULO → DECOMPOSIÇÃO → EVIDÊNCIA → CLAIM → NARRATIVA → DECISÃO`. Nunca: `DADOS + HISTÓRICO + LLM → NARRATIVA`.

## 2. O que NÃO fazer (resumo — lista completa fica condensada em references/checklist-redesenho.md)

- Não deixar o LLM ser a calculadora principal (cálculos, reconciliações, taxas, somas, comparação %, identificação do maior driver, validação matemática da própria resposta).
- Não usar narrativa histórica como evidência — histórico gera hipótese, contextualiza, sugere perguntas; nunca prova a causa do mês atual.
- Não transformar padrões observados em regras permanentes — nenhum padrão deve ter validade indefinida.
- Não confundir correlação com causa — "os dados são consistentes com X, mas não permitem atribuir causalidade a Y" é uma resposta válida e às vezes a correta.
- Não permitir narrativa sem reconciliação — se os impactos não reconciliam com a variação consolidada, a narrativa é bloqueada (`VALIDATION FAILED / Narrative blocked / Reason: bridge does not reconcile`), não publicada como se estivesse validada.
- Não permitir que o texto escolha o principal driver — o motor analítico decide (`primary_driver` no contrato de evidência); o LLM não pode contradizer isso sem declarar explicitamente uma inconsistência.
- Não esconder o cálculo intermediário — todo número importante precisa responder valor → fórmula → dados de entrada → período → fonte, em segundos.
- Não esconder o prompt atrás da interface, mas também não transformar a exibição do prompt numa simulação: se uma etapa não está realmente rodando, ela não deve ser apresentada como se estivesse.
- Não colocar segredo no frontend (API keys, tokens, credenciais, endpoints privados sensíveis) — a landing page mostra resultado e processo; credenciais ficam no backend.
- Não criar falsa sensação de tempo real — a interface só mostra estados que correspondem a uma execução real.
- Não transformar o projeto num dashboard genérico — a pergunta central continua sendo "como o agente chegou a essa história?", não "como colocar todos os KPIs numa tela".
- Não fazer over-engineering (arquitetura multiagente, vector database, RAG complexo, fine-tuning, MLOps, infraestrutura distribuída, workflow engine, dezenas de microsserviços) — se Python + API simples resolve, essa é a primeira implementação.
- Não usar RAG para resolver um problema que é de validação — se o agente acreditou demais no padrão histórico, o problema é a forma como o contexto influencia o raciocínio (contexto → hipótese, não contexto → verdade), não a qualidade da busca.
- Não usar apenas aprovação humana como métrica — testar contra casos conhecidos: driver accuracy, bridge reconciliation, unsupported claims, historical anchoring, human review time.
- Não testar apenas o caso fácil — construir pelo menos três: **Caso A** (padrão histórico confirmado — mix sobe, margem cai, o agente deve identificar o mix), **Caso B** (padrão histórico quebrado — mix cai, margem do Consignado sobe, Garantia cai, o agente deve abandonar a hipótese histórica), **Caso C** (dados insuficientes — dois drivers com impacto semelhante ou dado faltante; "não há evidência suficiente" é comportamento desejado, não falha).
- Não deixar recomendação parecer fato — separar explicitamente FATO / INTERPRETAÇÃO / HIPÓTESE / RECOMENDAÇÃO.
- Não inventar o dado que falta — "DADO AUSENTE", nunca "estimativa plausível".
- Não ignorar eventos fora do CSV (ex.: uma venda de carteira pontual) — evento conhecido ≠ impacto conhecido; não inventar um impacto financeiro que não está especificado.
- Não esconder incerteza — `Confidence: HIGH/MEDIUM/LOW`, mas confidence nunca substitui evidência.
- Não permitir que o checker valide a própria lógica sem teste independente — o teste precisa ter casos conhecidos com `assert` (`assert check_july() is True`, `assert check_august() is False`), virando teste de regressão.
- Não esconder falhas — se a nova versão errar, a interface mostra `FAILED / Expected: X / Agent: Y / Reason: ...`. O objetivo não é demonstrar uma IA perfeita, é demonstrar que o sistema detecta, explica, bloqueia ou sinaliza, e aprende com o erro de forma controlada.
- Não apagar a memória histórica — o problema não é ter memória, é tratar memória como verdade. Memória estruturada: `claim / period / direction / evidence / status / valid_until`.
- Não confundir "contar a história" com "descrever a variação" — a melhor saída aponta a pergunta de decisão para o próximo período, não só explica o número do mês.

## 3. Arquitetura mínima recomendada

```
Landing Page → Run Agent → API → Data Engine + Context → Bridge/Evidence → LLM → Checker → Final Story
```

Contrato mínimo entre camadas (o motor entrega ao LLM, nunca o contrário):

```json
{
  "period": "ago/26",
  "comparison_period": "jul/26",
  "margin": {"current": 9.90, "previous": 11.40, "delta": -1.50},
  "bu_contributions": [
    {"bu": "Garantia", "delta": -3.41},
    {"bu": "Consignado", "delta": 1.90}
  ],
  "primary_driver": "Garantia",
  "historical_hypotheses": [
    {"claim": "Mix Consignado pressiona margem", "status": "contradicted"}
  ]
}
```

## 4. Definição de pronto / teste principal

O protótipo só está pronto quando, com julho como contexto histórico e agosto como dado atual, o agente **rejeita** a hipótese histórica, aponta Garantia (não Consignado) como driver principal, reconhece o Consignado como contribuição positiva, e recomenda investigar se a compressão de spread é estrutural — em vez de repetir "a queda segue explicada pelo mix". Esse é o **Historical Anchoring Test**, e deve fazer parte da suíte de regressão.

## 5. Regra final

Sempre que houver conflito entre histórico e dado atual validado, **o dado atual vence**. Sempre que houver conflito entre narrativa e bridge, **a bridge vence**. Sempre que houver conflito entre conclusão desejada e evidência insuficiente, a resposta correta é **"não há dados suficientes para concluir"** — isso não é uma limitação do agente, é uma característica de qualidade.

## Adendo — sugestões recebidas junto com a especificação

- No one-pager/landing page, explicitar o método de decomposição da ponte (efeito isolado, mantendo os demais drivers constantes; atribuição de termos cruzados depende da ordem) para não deixar essa sutileza para um avaliador quantitativo atacar sozinho.
- Selo de interface: `DETERMINÍSTICO → cálculos`, `IA → narrativa`, `VALIDADOR → checker`, `HUMANO → decisão`.
