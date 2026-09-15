# Case FP&A Agêntico — o agente que conta a história dos números

## 1. Avaliação das narrativas

Recalculei a margem de contribuição por BU e por mês a partir dos drivers da seção 3.4, usando a fórmula das notas de apoio (receita, funding, custo de crédito e opex incidem sobre a **carteira média** ao mês — `carteira × taxa a.a. ÷ 12`; o CAC incide sobre a originação do mês). O resultado reconcilia de forma exata com os três totais consolidados dados no case (12,9 / 11,4 / 9,9), o que valida a fórmula e os dados:

| Mês | Garantia | Consignado | Consolidado (recalculado) | Consolidado (caso) |
|---|---:|---:|---:|---:|
| jun/26 | 11,91 | 0,99 | 12,90 | 12,9 |
| jul/26 | 12,29 | −0,88 | 11,41 | 11,4 |
| ago/26 | 8,88 | 1,02 | 9,90 | 9,9 |

**Narrativa de julho: correta.** A participação do Consignado na originação de fato saltou de 25,0% para 40,5%, e o Consignado operou com margem **negativa** (−0,88 mi) por causa do CAC (5,8% da originação, 2,6× o de Garantia). Garantia ficou estável no período (todos os drivers iguais a junho). O diagnóstico "mix de originação explica a queda" é sustentado pelos números.

**Narrativa de agosto: incorreta em dois pontos verificáveis.**

1. *"A queda segue explicada por mix de originação... padrão já observado em julho."* Falso: a participação do Consignado **caiu** de 40,5% para 28,7% em agosto — o mix moveu na direção oposta à de julho. E a margem do Consignado **melhorou** R$ 1,90 mi (de −0,88 para +1,02), porque a originação recuou de 75 para 45 e o CAC total caiu junto. Em agosto, o Consignado empurrou o consolidado para **cima**, não para baixo.
2. *"Garantia manteve comportamento estável no período."* Falso: a margem de Garantia caiu R$ 3,41 mi (12,29 → 8,88), sozinha mais que toda a queda consolidada (−1,5 mi). Decompondo o Δ de Garantia driver a driver (script `prototype_bridge.py`, mantendo os demais drivers no valor de julho e trocando um de cada vez):

| Driver | Efeito no Δ margem |
|---|---:|
| taxa média (28,0% → 26,4%) | −2,45 |
| custo de funding (13,0% → 13,6%) | −0,92 |
| custo de crédito (4,5% → 4,6%) | −0,15 |
| originação/CAC | −0,04 |
| carteira média (volume) | +0,16 |
| **soma** | **−3,41** |

A queda de agosto é quase inteiramente **compressão de spread em Garantia** (taxa caindo, funding subindo), não mix entre BUs. O Consignado foi, na verdade, o único alívio do mês.

## 2. Causa raiz

O erro não está no cálculo — está em **como a explicação é produzida e reaproveitada**. Três coisas se combinam:

- **O pipeline funde cálculo e narração num único passo** (item [3]: "o CSV e o repositório entram no prompt... o agente calcula as variações e escreve a narrativa"). Não existe um artefato numérico intermediário, auditável, que alguém possa conferir em segundos — só o texto final. Isso empurra a verificação para dentro da cabeça de quem lê.
- **O repositório de contexto acumula "padrões observados" como frases soltas, sem prazo de validade nem teste de recorrência.** A entrada `[jul/26] quedas de margem... têm sido explicadas por mix de originação` e a `regra de leitura: começar a análise pelo mix de originação entre BUs` viram um *prior* que o agente aplica de novo em agosto — e o resultado de agosto (aprovado) vira mais uma entrada reforçando a mesma leitura, mesmo estando errada. O sistema tem memória, mas não tem *esquecimento* nem *falsificação*: nada nele testa se o padrão de julho ainda vale em agosto antes de repeti-lo.
- **A revisão humana de 10 minutos é uma checagem de plausibilidade, não de reconciliação.** Depois de dois meses seguidos vendo "Consignado pressiona, Garantia está estável", a narrativa de agosto soa exatamente como o analista espera — é coerente com a memória recente, não com a planilha. Ninguém tem, nesses 10 minutos, um jeito rápido de comparar "o texto diz X" com "os números dizem Y"; a única forma de pegar o erro seria recalcular a ponte na mão, o que anula o ganho de tempo que motivou o projeto.

Em resumo: o agente não errou a conta, errou a **atribuição causal** — e o desenho do sistema (memória que se autorreforça + revisão só de texto) garante que esse tipo de erro sobrevive.

## 3. Redesenho

Duas decisões, ambas implementadas no protótipo (`prototype_bridge.py`):

**Decisão 1 — separar cálculo de narração; a ponte numérica é obrigatória e vem antes do texto.** O agente passa a produzir, a cada mês, uma ponte estruturada (Δ margem por BU e, para o BU com maior Δ, por driver) *antes* de qualquer frase ser escrita. A narrativa é gerada como uma leitura dessa ponte, não como uma reconstrução livre a partir do CSV. Isso transforma "a IA calculou e escreveu" em duas etapas auditáveis separadamente — e a segunda etapa (a prosa) fica proibida de citar como causa principal um BU/driver que não seja o de maior módulo na ponte.

**Decisão 2 — claims do repositório passam a ser estruturadas e falsificáveis, não texto livre.** Em vez de `[jul/26] quedas de margem... têm sido explicadas por mix`, o repositório guarda `{driver: "consignado_mix", direção_esperada: "negative", mês: "jul/26"}`. A cada novo mês, antes de qualquer claim antiga poder ser citada como "padrão recorrente", ela é testada contra a ponte do mês corrente. Se contradita, é marcada como encerrada e não pode mais ser reutilizada — o repositório para de crescer "sozinho" na direção errada.

**A prova (não a intenção):** rodei o checker das duas decisões contra as claims extraídas literalmente das narrativas reais de julho e agosto do case. É um teste de regressão com gabarito conhecido — já sabemos que agosto está errado e julho está certo, então o checker *tem* que separar os dois:

```
[PASS] narrativa jul/26 — Consignado Δ=-1,87 é o termo dominante, como a claim afirma.
[FAIL] narrativa ago/26 — Consignado teve Δ=+1,90 (sinal contrário); o termo
        dominante foi 'garantia' (Δ=-3,41), não Consignado.
```

O script roda (`python3 prototype_bridge.py`) e termina com `assert` explícito nesse resultado — se uma mudança futura no checker deixar de pegar o erro de agosto, o teste quebra sozinho. Esse é o critério de "funciona": não é o texto ficar mais bonito, é o sistema reprovar automaticamente a mesma classe de erro que passou pela revisão humana em produção.

## 4. Riscos e limites

- **A decomposição sequencial (bridge) depende da ordem dos drivers.** Trocar carteira, depois taxa, depois funding... aloca os termos cruzados de um jeito; outra ordem daria números levemente diferentes (efeito conhecido de decomposições Volume-Price-Mix). Para este case a ordem não muda a conclusão (taxa e funding dominam em qualquer ordem razoável), mas em situações mais apertadas isso pode enganar. Um decomposição tipo Shapley resolveria a ambiguidade, mas custa mais para calcular e explicar — não fiz essa troca aqui por não valer o custo neste volume de drivers.
- **O checker de claims é intencionalmente simples (baseado em claims estruturadas, não em NLP sobre o texto livre da narrativa).** Isso o torna confiável e testável, mas significa que alguém (hoje, eu; depois, o próprio agente na etapa de geração) precisa extrair a claim estruturada da narrativa — não é uma auditoria automática de texto solto.
- **Eventos não recorrentes (como a venda de carteira de R$ 150 mi em Garantia, 29/ago) não entram no CSV de drivers e não teriam sido vistos pelo agente novo ou pelo antigo.** Neste mês isso não distorceu o cálculo (a carteira média de agosto mal se move com um evento em 29/ago), mas é um ponto cego real: nada no pipeline atual injeta eventos qualitativos no contexto do mês corrente.
- **Só existem três meses de dado para validar.** O teste de regressão prova que o checker pega *este* erro real; não prova que os limiares (o que conta como "termo dominante") generalizam bem para 12+ meses de histórico com mais ruído.
- **A Decisão 2 (claims estruturadas com expiração) é mudança de processo, não só de código** — exige que quem aprova a narrativa também aprove/edite a claim estruturada correspondente. Tem atrito de adoção que o protótipo não testa.

## 5. Upgrade — a pergunta que devia estar sendo feita

Duas narrativas seguidas descreveram a variação sem provocar decisão nenhuma além de "revisitar o incentivo do Consignado" — e mesmo essa recomendação estava presa a um diagnóstico errado em agosto. A pergunta que os números de agosto realmente levantam não é "por que a margem caiu", é: **o spread de Garantia, que ficou parado quatro meses, acabou de comprimir 160 bps em taxa e 60 bps em funding no mesmo mês — isso é um cliente/negociação pontual ou o início de uma reprecificação que vai continuar em setembro?** Essa é a pergunta que a liderança precisa decidir, e ela ficou invisível porque a história repetida do Consignado (que, em agosto, era na verdade uma boa notícia) ocupou todo o espaço da narrativa.

---

## Anexo de processo

**Prompts principais usados** (nesta conversa, com Claude): pedi para ler o PDF do case com atenção; em seguida pedi para reconstruir e validar os números com código antes de escrever qualquer diagnóstico, em vez de confiar na leitura das narrativas de prosa; depois pedi a decomposição driver-a-driver do Δ de Garantia entre julho e agosto; por fim pedi para transformar o redesenho num protótipo que rodasse e testasse a própria alegação da narrativa de agosto contra os dados reais.

**O que a IA errou ou entregou raso, e o que foi feito a respeito:** a primeira tentativa de decomposição usei a carteira "quanto ao início do mês" por hábito — não bateu com os totais consolidados dados no case. Troquei para carteira média (que a nota de apoio já indicava) e conferi que reconciliava exatamente com os três totais (12,9 / 11,4 / 9,9) antes de seguir para qualquer conclusão qualitativa; sem essa reconciliação eu não teria confiança para afirmar que a narrativa de agosto está errada, só que "parece estranha".

**O que foi descartado pelo caminho:** (1) uma decomposição tipo Shapley value para os drivers de Garantia — mais robusta contra ambiguidade de ordem, mas cara de explicar e desnecessária para 6 drivers onde um checkup de ordem única já mostra taxa e funding dominando por margem larga; (2) um checker baseado em parsing de linguagem natural da narrativa (em vez de claims estruturadas) — descartado porque seria menos confiável e mais difícil de testar de forma determinística dentro do prazo do case; (3) incluir o evento da venda de carteira no modelo de atribuição — descartado porque, checando os números, ele não move a carteira média de agosto o suficiente para explicar o Δ observado; documentei isso como ponto cego em vez de simular um efeito que os dados não sustentam.

**Iteração do protótipo:** a primeira versão (`prototype_bridge.py`) só tinha a ponte e um checker de claims soltas. Depois de revisar o redesenho com mais detalhe — separar DADO→CÁLCULO→EVIDÊNCIA→NARRATIVA→DECISÃO como contrato explícito, e nunca deixar o histórico virar regra permanente — reescrevi o motor em `agent_engine.py` com um evidence contract estruturado, memória histórica com status testável a cada rodada (`confirmed_for_period` / `contradicted`) e três casos de teste (A: padrão confirmado, B: padrão quebrado — o caso real de agosto, C: evidência insuficiente, cenário sintético). O teste mais revelador não estava no plano original: rodar o checker contra o texto **real e literal** da narrativa de agosto do case (não uma paráfrase) faz o checker reprovar por "historical anchoring" — a mesma classe de erro que a revisão humana de 10 minutos deixou passar em produção. A landing page interativa (`agente_fpa_landing.html`) expõe esse motor com um seletor de contexto v1.0 (agente antigo) vs. v2.0 (redesenho): rodar ago/26 com v1.0 reproduz e reprova a narrativa real; com v2.0, a hipótese histórica é testada e corretamente rejeitada antes de qualquer texto ser aceito.
