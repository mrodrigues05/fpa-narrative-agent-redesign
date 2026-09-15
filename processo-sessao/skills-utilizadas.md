# Skills utilizadas nesta sessão

Lista honesta — só o que foi de fato consultado/usado, na ordem em que entrou.
Skills do Claude vivem em `/mnt/skills/public/<nome>/SKILL.md`; a instrução do
meu ambiente é ler o SKILL.md relevante antes de criar qualquer arquivo do
tipo que ele cobre.

## `frontend-design`

Lida antes do primeiro one-pager HTML (item 2 da recapitulação). Orienta
paleta com uma cor dominante + acento, tipografia com contraste (serifa de
destaque + sem-serifa de corpo), e uma lista explícita de clichês de IA a
evitar (faixas de cor decorativas, fundo creme genérico, negrito em excesso).
É a base de todo o sistema visual usado depois — cores da marca, Source Serif
4 + Inter no HTML, e a mesma lógica (adaptada pras fontes seguras) no PPT.

## `xlsx`

Lida antes de criar `margem.xlsx` (item 4). Define as convenções seguidas:
fonte Arial, azul para inputs brutos, preto para fórmulas, formatação
percentual explícita — e o passo que é fácil esquecer e que segui à risca:
depois de escrever fórmulas com `openpyxl`, é obrigatório recalcular com
`scripts/recalc.py` antes de qualquer leitor (Python `data_only=True` ou
SheetJS no navegador) conseguir ver os valores, não só as fórmulas em texto.

## `skill-creator`

Consultada na construção do pacote reaproveitável (item 8): estrutura de uma
skill (SKILL.md com frontmatter `name`/`description`, `references/` para
detalhe pesado, `templates/`/`examples/` para material de apoio), e o
princípio de manter o SKILL.md compacto e apontar pra fora em vez de acumular
tudo num arquivo só.

## `pptx`

Lida antes de construir `case_vertice_apresentacao.pptx` (item 9). Várias
decisões vieram direto dali: usar `pptxgenjs` para criar do zero; fontes
seguras (Cambria + Calibri) porque nomes de fonte só renderizam de verdade no
PowerPoint de quem abre, não neste ambiente; nunca usar faixa/listra de cor
como "motivo" decorativo; e o processo de QA obrigatório — validar o arquivo
(`scripts/office/validate.py`), converter pra imagem
(`scripts/office/soffice.py` + `pdftoppm`) e olhar cada slide. Foi essa QA que
pegou os dois problemas reais do gráfico do slide 4 (cores invertidas e
rótulos colidindo) antes de qualquer coisa chegar até você.

## O que não foi usado

`docx`, `pdf` (criação), `pdf-reading`/`file-reading` (o PDF do case chegou
como conteúdo direto na conversa, não precisou ser lido do disco),
`product-self-knowledge`, `import-memory`, `morning`, e as skills de plugin do
Cowork — nenhuma tinha relação com o que foi pedido nesta sessão.
