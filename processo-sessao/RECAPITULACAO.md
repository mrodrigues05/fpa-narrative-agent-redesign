# Recapitulação da sessão

Registro cronológico do que foi pedido e entregue nesta conversa — o case
Vértice (FP&A) do zero até a apresentação final. Serve como o "anexo de
processo" em formato mais longo: mostra as decisões, os erros achados no
caminho, e como cada entregável nasceu do anterior.

## 1. O case chega

Upload do PDF "Case Técnico — Estágio em Desenvolvimento de Projetos com IA".
Pedido: avaliar um agente de IA que gera, todo mês, a narrativa de variação da
margem de contribuição de uma fintech fictícia (Vértice, BUs Garantia e
Consignado) — e propor o que fazer com ele. Entregável formal: um `.md` de até
4 páginas + anexo de processo.

## 2. Diagnóstico e primeira entrega

Recalculei a margem por BU e por mês a partir dos drivers brutos (não confiei
na prosa das narrativas). O recálculo reconciliou exatamente com os totais do
case (12,9 / 11,4 / 9,9), o que validou a fórmula antes de qualquer conclusão
qualitativa. Resultado: a narrativa de julho está correta; a de agosto está
errada em dois pontos verificáveis — o mix do Consignado caiu (não subiu) e
sua margem melhorou, enquanto 100% da queda veio de compressão de spread em
Garantia.

Entreguei: `case_vertice_fpa.md` (avaliação, causa raiz, redesenho com 2
decisões, riscos, upgrade, anexo de processo) + `prototype_bridge.py` (motor
v1: ponte + checker de claims soltas) + um one-pager HTML estático com a
identidade visual da Creditas (a empresa por trás do processo seletivo).

## 3. Especificação estendida — protótipo interativo

Você colou dois documentos-fonte mais detalhados ("Skill — Agente FP&A que
Conta a História dos Números" e "Agente FP&A Vértice") pedindo um protótipo de
verdade: painel Agent Run, pipeline visual passo a passo, prompt viewer,
Evidence Board, Narrative Check, teste adversarial, memória histórica como
claims falsificáveis. Reescrevi o motor (`agent_engine.py` v2) com um evidence
contract estruturado e memória com status testável, e construí
`agente_fpa_landing.html`: a mesma engine em JavaScript, com um botão que
chama a API da Anthropic ao vivo (com fallback automático pro modo
determinístico) e um "Run Adversarial Test" que reproduz o caso real de
agosto.

## 4. Dados em planilha, não embutidos no código

Pedido: mais realista ter os dados num Excel. Criei `margem.xlsx` (abas
Garantia/Consignado, linha de margem como **fórmula viva**, aba Consolidado
que confere reconciliação sozinha) e reescrevi o `agent_engine.py` pra ler
dali — com erro alto e claro (`DADO AUSENTE`) se o arquivo não existir, em vez
de estimar. Na landing page, adicionei um campo de upload (.xlsx) via SheetJS,
já que o navegador não pode ler um arquivo local sem ação explícita do
usuário.

## 5. Entendimento técnico e prova

Você pediu pra entender a fundo como o motor funciona e como provar que ele
não falha. Expliquei o pipeline função por função (fórmula, ponte, evidence
contract, validação de hipótese, checker) e rodei, ao vivo, o teste mais forte
que tínhamos: o checker contra o **texto real e literal** da narrativa de
agosto do case — resultado `FAIL`, pego pelo teste de historical anchoring.

## 6. Ajustes na landing page

Trocamos o idioma da barra superior para português, o wordmark de "creditas"
para "Vértice" (nome fictício do case), adicionamos um gráfico de linha de
tendência em Evidências — e depois você pediu pra tirar esse gráfico por
completo, o que fiz removendo container, função e as três chamadas, sem deixar
rastro.

## 7. Um bug real, achado por você

Testando a página, você reportou que `v1.0 · offline` estava passando
(`PASS/HIGH`) num caso que deveria falhar. O bug: `hyps` só era calculado
quando `contexto==='v2.0'` — com `v1.0`, o array ficava vazio e o checker de
historical anchoring não tinha nada pra testar, então passava por ausência de
dado, não por estar certo. Corrigido computando `hyps` sempre, independente do
contexto — o checker precisa validar toda narrativa, não só a que ele já
esperava reprovar.

## 8. A skill reaproveitável

A pedido, empacotei o método (não o case específico) numa skill:
`SKILL.md` + `references/checklist-redesenho.md` (condensado dos dois
documentos-fonte) + `templates/` (motor, planilha e documento genéricos, com
seções "AJUSTE AQUI") + `examples/` (o case Vértice inteiro, resolvido, como
referência) + `docs-originais/` (os dois documentos-fonte, preservados na
íntegra). Testei o template genérico apontando pra mesma planilha do Vértice
antes de entregar — reproduziu os mesmos números.

## 9. Documentação de uso e apresentação

Escrevi `README.md` (como preparar o ambiente, rodar o motor, abrir a landing
page dentro e fora do Claude, checklist pré-apresentação) e construí
`case_vertice_apresentacao.pptx` — 10 slides seguindo os 5 itens do case,
paleta e tipografia do HTML adaptadas pras fontes seguras do PowerPoint
(Cambria + Calibri), com um gráfico nativo da ponte de Garantia e um slide
dedicado mostrando o bug do item 7 como código antes/depois, como validação.

## 10. Slide do bug — reenquadrado

Você corrigiu o enquadramento do slide 7 do PPT: o "antes" não devia ser
código nenhum, porque o agente antigo não tinha código — tinha uma regra em
texto livre dentro do repositório de contexto (`padroes-margem.md`). Troquei
o "antes" pra citar essa regra real do case, e o "depois" pra mostrar a
função `validate_hypothesis()` de verdade — o slide passou a ilustrar a
Decisão 2 do redesenho, não um bug interno da nossa própria ferramenta.

## 11. Chamada de LLM ao vivo — adicionada, depois removida

Você pediu pra rodar o código via API de verdade antes da entrevista. Expliquei
duas formas (o modo "Ao vivo" já embutido na landing page, e um script novo,
`run_live_narrative.py`, que chamava a API pelo terminal com a chave do próprio
usuário) e testei tudo que dava pra testar sem gastar uma chamada real. Na
sequência, você decidiu não usar chamada de API nenhuma, pra não ter custo.
Removi o modo "Ao vivo" por completo da landing page (a função `callLLM`, o
seletor de modo, o fallback, as menções no rodapé) — o protótipo agora é 100%
determinístico, sem nenhuma chamada de rede, e apaguei o script standalone.

## 12. Esta pasta

`processo-sessao/` — esta recapitulação, `skills-utilizadas.md`, e `json/` com
a saída real do motor (não fabricada) para os três casos de teste, a memória
histórica e o schema do evidence contract — gerados rodando `agent_engine.py`
de novo, agora, antes de escrever este arquivo.
