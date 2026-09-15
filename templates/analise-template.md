# Case [nome do agente/empresa] — [uma frase resumindo o achado principal, no estilo "a queda não foi X, foi Y"]

## 1. Avaliação das narrativas
[Recalcule o KPI por unidade/segmento e por período a partir dos drivers brutos. Mostre a tabela de
reconciliação contra qualquer total de referência dado no case — ela precisa bater antes de você
concluir qualquer coisa qualitativa. Para cada narrativa fornecida, diga se está correta ou não, e
sustente com os números recalculados, não com impressão.]

## 2. Causa raiz
[Onde cálculo e narração se misturam num único passo sem artefato auditável; como o repositório de
contexto virou regra permanente em vez de hipótese testável; o que a revisão humana consegue checar
no tempo que tem (normalmente não dá pra recalcular nada — só ler se soa coerente com o que já se
esperava ver).]

## 3. Redesenho
[2 a 3 decisões, cada uma com uma frase de justificativa — não uma lista de dez ideias genéricas.
Termine com a prova: o resultado real do checker rodando contra os casos A (padrão confirmado),
B (padrão quebrado/adversarial) e C (evidência insuficiente). Descreva o teste, não a intenção.]

## 4. Riscos e limites
[O que a decomposição/checker não resolve — ambiguidade de ordem numa decomposição sequencial,
dependência de claims estruturadas extraídas manualmente, eventos fora do dado bruto, tamanho da
amostra disponível para validar limiares.]

## 5. Upgrade (opcional)
[A pergunta de decisão que a liderança deveria estar respondendo — não a descrição da variação.
Geralmente é sobre o driver que ficou "estável" por vários períodos e que, exatamente no período do
case, deixou de estar.]

---

## Anexo de processo
[Prompts principais usados; o que a IA errou ou entregou raso e o que foi feito a respeito; o que foi
descartado pelo caminho (ex.: uma decomposição mais robusta mas cara demais de explicar; um checker
baseado em NLP em vez de claims estruturadas). Este anexo é avaliado, não fiscalizado — mostrar uma
tentativa que falhou e por que vale mais que uma entrega limpa sem rastro.]
