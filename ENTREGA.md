# Entrega — o que foi pedido e o que foi entregue

Este arquivo existe só pra deixar explícito, ponto a ponto, como esta
entrega atende ao formato pedido no case. Ele **não é** o documento
avaliado — é um mapa de navegação. O documento avaliado é
[`motor-fpa/case_vertice_fpa.md`](motor-fpa/case_vertice_fpa.md).

## O que foi pedido (formato da entrega, conforme o enunciado)

> **7. Formato da entrega**
> Um único arquivo .md, até 4 páginas, mais o anexo de processo. Se houver
> protótipo, mande o código ou o link junto.
> O arquivo .md é o que será avaliado. A apresentação é separada e o
> formato é livre — slides, tela compartilhada, quadro, só falando. Use o
> que te deixa mais confortável para defender o raciocínio.
>
> **Anexo de processo (obrigatório).** No fim do mesmo arquivo, registre:
> - os prompts principais que você usou;
> - o que a IA errou ou entregou raso, e o que você fez a respeito;
> - o que você descartou pelo caminho.
> Esse anexo é avaliado, não fiscalizado. Um anexo mostrando três
> tentativas que falharam vale mais do que uma entrega limpa sem rastro.
>
> Apresentação: 10 minutos, seguidos de 5 minutos de perguntas.
>
> **8. Critérios de avaliação**
> - Qualidade da leitura do dado
> - Qualidade do diagnóstico e do raciocínio que levou até ele
> - Verificabilidade do que você propõe
> - Pragmatismo — solução enxuta contra over-engineering
> - Honestidade sobre os próprios limites
> - Clareza, no documento e na defesa oral

## Como esta entrega atende cada ponto

| Exigência | Atendida em |
|---|---|
| Um único arquivo `.md`, até 4 páginas | [`motor-fpa/case_vertice_fpa.md`](motor-fpa/case_vertice_fpa.md) — é o **único** arquivo avaliado; todo o resto do repositório é apoio/rastreabilidade, não substitui nem complementa a nota. |
| Anexo de processo, no fim do mesmo arquivo | Seção **"Anexo de processo"**, ao final de [`case_vertice_fpa.md`](motor-fpa/case_vertice_fpa.md#anexo-de-processo) — prompts principais, o que a IA errou/entregou raso e o que foi feito a respeito, o que foi descartado pelo caminho. |
| Se houver protótipo, mande o código ou o link | Os dois: protótipo publicado ao vivo em **https://mrodrigues05.github.io/fpa-narrative-agent-redesign/**, e código-fonte completo em **https://github.com/mrodrigues05/fpa-narrative-agent-redesign**. |
| Verificabilidade do que se propõe | Motor determinístico com 3 casos de teste + `assert` ([`motor-fpa/agent_engine.py`](motor-fpa/agent_engine.py)) — roda em terminal (`python agent_engine.py`) ou ao vivo na landing page, reproduzindo os mesmos números citados no documento avaliado. |
| Honestidade sobre os limites | Seção **"4. Riscos e limites"** de [`case_vertice_fpa.md`](motor-fpa/case_vertice_fpa.md). |

## Links diretos

- **Documento avaliado:** [`motor-fpa/case_vertice_fpa.md`](motor-fpa/case_vertice_fpa.md)
- **Protótipo interativo (ao vivo):** https://mrodrigues05.github.io/fpa-narrative-agent-redesign/
- **Repositório / código-fonte:** https://github.com/mrodrigues05/fpa-narrative-agent-redesign
- **Motor determinístico (Python, roda em terminal):** [`motor-fpa/agent_engine.py`](motor-fpa/agent_engine.py)
- **Como rodar tudo localmente:** [`README.md`](README.md)

## O que existe no repositório além do documento avaliado (e por quê)

Nada disso é exigido pelo formato de entrega — está aqui só como
rastreabilidade e apoio, caso alguém queira aprofundar antes ou depois da
apresentação:

| Pasta/arquivo | Conteúdo |
|---|---|
| `motor-fpa/` | O protótipo em si: motor Python, planilha de dados, landing page interativa. |
| `processo-sessao/` | Recapitulação cronológica da sessão que gerou este material, skills do Claude usadas, e os `.json` reais (evidence contracts e resultados do checker) dos 3 casos de teste. |
| `docs-originais/` | Os documentos-fonte completos (especificação da landing page e princípios de redesenho) preservados na íntegra. |
| `SKILL.md` | O framework reutilizável para redesenhar agentes de narrativa financeira em outros cases parecidos. |
| `templates/` | Versões genéricas (não específicas do case Vértice) do motor, do gerador de planilha e do documento de análise. |
| `technical_case_strategy_framework.json` | O schema de estratégia usado para conduzir a colaboração ao longo do case. |
| `Guia-Simples-Nao-Tecnico.docx` | Explicação do projeto sem jargão técnico, para público leigo. |
