# Skill — Agente FP&A que Conta a História dos Números

*Documento-fonte colado no chat durante a construção desta skill — a especificação
completa do painel Agent Run, do pipeline visual, do prompt viewer e da
arquitetura recomendada (landing page → API → LLM → validador). Preservado aqui
na íntegra por rastreabilidade; o `SKILL.md` já destila o que dele virou fluxo
de trabalho, e `examples/landing_reference.html` é a implementação que resultou
desta especificação.*

## Objetivo

Construir um protótipo de agente de IA para FP&A capaz de transformar dados financeiros mensais em uma narrativa executiva verificável.

O agente deve responder a três perguntas:

1. O que aconteceu com a margem?
2. Por que aconteceu?
3. O que isso deveria fazer a liderança investigar ou decidir?

A solução deve preservar o contexto original do case: a Vértice possui duas BUs — Garantia e Consignado — e o time de FP&A precisa explicar mensalmente a variação da margem de contribuição consolidada. O projeto deve avaliar e redesenhar o agente existente, não simplesmente criar um dashboard financeiro.

## Princípio central

A solução deve separar:

DADO → CÁLCULO → EVIDÊNCIA → RACIOCÍNIO → NARRATIVA → DECISÃO

O LLM não deve ser tratado como calculadora ou fonte de verdade. A matemática e as reconciliações devem ser determinísticas. O LLM deve transformar evidências já calculadas em narrativa executiva. Histórico pode gerar hipóteses, mas não pode ser utilizado como evidência causal sem validação no período atual.

## Protótipo interativo obrigatório

A landing page deve funcionar também como uma demonstração do agente, com uma seção "Agent Run — veja o agente trabalhando", onde o avaliador seleciona mês de análise, mês de comparação, versão do contexto e modo de execução, e clica em "Executar análise".

### Pipeline visual

A execução deve aparecer como uma rotina real:

```
01  ✓ Carregando dados
02  ✓ Calculando margem por BU
03  ✓ Decompondo variação
04  ✓ Comparando com histórico
05  ✓ Construindo evidências
06  ● Executando prompt
07  ○ Validando narrativa
08  ○ Gerando recomendação
```

Isso é importante porque permite ao avaliador visualizar que o LLM não está recebendo simplesmente `CSV + prompt → texto`, mas sim `CSV → motor analítico → evidências → LLM → validação`.

### Visualização do prompt

A landing page deve possuir uma área "Prompt em execução" onde o usuário pode expandir o prompt utilizado, com SYSTEM / CONTEXT / DATA / EVIDENCE / TASK / OUTPUT destacados visualmente. Não é necessário expor chaves, tokens, credenciais ou informações secretas.

## Arquitetura técnica

Dois modos de execução: notebook/VS Code (desenvolvimento, testes e auditoria) e landing page. A landing page não deve executar diretamente credenciais ou chamadas privadas de IA no navegador; a arquitetura recomendada é `LANDING PAGE → POST /run-agent → BACKEND/API (lê CSV, executa cálculos, gera evidências, monta prompt, chama LLM, valida resposta) → STREAM DE EXECUÇÃO → LANDING PAGE`. Para o protótipo, um backend pequeno em Python/FastAPI é suficiente — não é necessário construir infraestrutura de produção.

### Atualização simultânea

Cada execução deve gerar um Run ID e atualizar a landing page com os resultados daquela execução (margem, variação, principal contribuição por BU, status de reconciliação/evidência/narrativa). Server-Sent Events ou polling simples bastam — não criar uma arquitetura de streaming complexa apenas para efeito visual, nem uma falsa sensação de tempo real: a interface só deve mostrar estados que correspondem a uma execução real.

## Evidência antes da narrativa

A landing page deve mostrar a estrutura intermediária que normalmente ficaria invisível — um "Evidence Board" com a margem consolidada, a contribuição por BU, o mix de originação e os drivers da BU dominante — antes de qualquer conclusão em prosa aparecer.

## Validação automática

Depois que o LLM gerar a narrativa, um segundo estágio ("Narrative Check") verifica: reconciliação (a soma dos impactos explica a variação consolidada?), evidência (cada afirmação causal tem lastro?), consistência (a narrativa contradiz os dados?), histórico (está repetindo um padrão anterior sem evidência atual?) e limitações (o agente está afirmando algo que os dados não permitem concluir?). Resultado esperado, por exemplo: `✓ Matemática consistente / ✓ Variação reconciliada / ✓ Driver principal suportado / ⚠ Recomendação comercial requer dado adicional / Confidence: HIGH`.

## Histórico como memória auditável

O repositório de contexto continua existindo, mas muda de papel: em vez de "Regra: começar pelo mix", vira uma "Historical Hypothesis" com período, evidência de origem, resultado ("Confirmado para Jul/26") e status ("HIPÓTESE HISTÓRICA — não utilizar como causa sem validação no período atual"). A landing page pode mostrar essa diferença numa aba "Current Evidence | Historical Context".

## Reprodutibilidade

Cada execução gera um Run ID e registra data, período, versão dos dados, versão do contexto, versão do prompt, modelo utilizado, resultado dos cálculos, narrativa gerada e resultado da validação — para que "por que escrevemos isso em agosto?" possa ser respondido reconstruindo a execução.

## O que NÃO fazer

Não virar dashboard genérico de BI, chatbot financeiro, sistema multiagente complexo, plataforma de MLOps, projeto de infraestrutura, ou uma interface que apenas simula uma execução. Prioridade: **correção > verificabilidade > transparência > experiência visual > sofisticação técnica.**

## Critério de sucesso

Rodado com julho como contexto histórico e agosto como período atual, o agente deve **rejeitar** a hipótese histórica de mix como explicação da queda, apontando Garantia (não Consignado) como driver principal, com Consignado como offset positivo, e sinalizando explicitamente a limitação sobre por que a taxa de Garantia caiu (dado não disponível no case). Esse teste é o principal proof of concept do redesenho.

## Adendo — sugestões recebidas junto com a especificação

- Adicionar dois botões de execução: "▶ Run Agent" e "⚡ Run Adversarial Test" — o segundo roda automaticamente o caso crítico de agosto, em que o contexto histórico tenta induzir o agente ao erro, mostrando explicitamente `Agent decision: ✕ Reject historical hypothesis`.
- Explicitar na metodologia que a ponte (bridge) é uma decomposição de efeito isolado (mantendo os demais drivers constantes) e que a atribuição dos termos cruzados depende da ordem escolhida — para não deixar essa sutileza para um avaliador mais quantitativo descobrir sozinho.
- Um selo simples na interface: `DETERMINÍSTICO → cálculos` / `IA → narrativa` / `VALIDADOR → checker` / `HUMANO → decisão`.
