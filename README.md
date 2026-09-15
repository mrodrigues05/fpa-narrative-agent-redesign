# Como usar este case — preparação de ambiente e passo a passo

Este documento explica como rodar os três artefatos técnicos do case
(`agent_engine.py`, `margem.xlsx`, `agente_fpa_landing.html`) a partir do zero,
sem depender de nada além do que está descrito aqui.

## 1. O que cada arquivo faz

| Arquivo | Papel |
|---|---|
| `case_vertice_fpa.md` | O documento avaliado — avaliação das narrativas, causa raiz, redesenho, riscos, anexo de processo. |
| `margem.xlsx` | A fonte de dados. Abas "Garantia" e "Consignado" com os drivers brutos; a linha de margem é **fórmula**, não valor colado. |
| `agent_engine.py` | O motor determinístico em Python: lê `margem.xlsx`, recalcula a margem, monta a evidência, testa a hipótese histórica e roda o checker contra 3 casos (A confirmado, B adversarial/agosto, C evidência insuficiente). |
| `agente_fpa_landing.html` | A demonstração interativa do mesmo motor, em JavaScript, com painel "Execução do Agente". |

Os três primeiros já vêm prontos. Este documento é sobre como colocá-los pra rodar.

## 2. Preparar o ambiente

Você precisa de **Python 3.9 ou mais recente**. Verifique:

```bash
python3 --version
```

O único pacote externo usado é o `openpyxl` (lê o `.xlsx`). Se o comando abaixo
der erro de import, instale:

```bash
pip install openpyxl
```

Nenhum outro pacote, chave de API, ou serviço externo é necessário para rodar
o script Python. Para a landing page, basta um navegador — não precisa de
servidor, Node, nem instalação de nada.

## 3. Rodar o motor (prova em terminal)

Coloque `agent_engine.py` e `margem.xlsx` **na mesma pasta** e rode:

```bash
python3 agent_engine.py
```

Saída esperada (resumo): os três casos (A, B, C) imprimem a evidência
recalculada, o status da hipótese histórica, a narrativa e o resultado do
checker, terminando em:

```
OK — hipótese confirmada em A, contradita em B, driver correto identificado,
     e evidência ambígua do Caso C não vira um driver inventado.
```

Se você mudar qualquer número em `margem.xlsx`, precisa **recalcular as
fórmulas** antes de rodar o script de novo — o Excel só grava o valor
calculado quando alguém (Excel, LibreOffice, ou um script) abre e recalcula o
arquivo. Se você editou a planilha num programa de planilha normal (Excel,
Google Sheets, LibreOffice Calc) e salvou, já está recalculado — não precisa
fazer nada extra. Isso só importa se você gerar/editar o `.xlsx` via script.

### Erros esperados e o que significam

| Erro | Causa | O que fazer |
|---|---|---|
| `FileNotFoundError: DADO AUSENTE: não encontrei '.../margem.xlsx'` | O script não achou a planilha na mesma pasta. | Copie `margem.xlsx` pra pasta do script. |
| `ValueError: DADO AUSENTE: driver 'X' não encontrado` | Uma linha da planilha foi renomeada ou apagada. | Confira se os rótulos da coluna A da aba continuam com as palavras-chave esperadas (ex.: "taxa", "funding", "cac"...). |
| `ModuleNotFoundError: No module named 'openpyxl'` | Pacote não instalado. | `pip install openpyxl`. |

## 4. Abrir a landing page

Só um jeito, e funciona em qualquer lugar: dê duplo clique no arquivo
`agente_fpa_landing.html` — ele abre em qualquer navegador, sem instalar
nada e sem depender de internet. Todo o motor roda no seu próprio navegador
(JavaScript puro) e a narrativa vem de um template determinístico — não há
nenhuma chamada de API, então não há custo nem dependência de rede.

### Usando o painel "Execução do Agente"

1. Escolha **Período atual** e **Comparação** (o par de meses a analisar).
2. Escolha **Contexto**: `v1.0` reproduz o agente antigo (regra fixa, sempre
   cita mix); `v2.0` é o redesenho (testa a hipótese contra o dado atual).
3. Clique **▶ Executar análise**, ou **⚡ Run Adversarial Test** pra já rodar
   direto o caso crítico (agosto vs. julho) com o contexto v2.0.
4. Acompanhe o pipeline rodando passo a passo, abra o prompt em execução (ele
   monta o SYSTEM + CONTEXT + EVIDENCE + TASK completo, só não envia a
   nenhuma API), e confira o resultado em Evidências → Narrativa → Validação.

### Carregando uma planilha diferente

No topo do painel Agent Run tem um campo "Fonte de dados". Sem nada
selecionado, a página usa os números de exemplo embutidos (iguais aos do
`margem.xlsx`). Se você carregar um `.xlsx` no mesmo formato (abas "Garantia"
e "Consignado", mesmos rótulos de driver), a página substitui os dados e os
seletores de mês se atualizam sozinhos.

## 5. Checklist antes da apresentação

- [ ] `python3 agent_engine.py` roda sem erro e termina em "OK".
- [ ] `agente_fpa_landing.html` abre (duplo clique, qualquer navegador) e o
      botão "⚡ Run Adversarial Test" mostra o painel de rejeição da hipótese
      histórica.
- [ ] `margem.xlsx` está na mesma pasta de `agent_engine.py`, caso alguém peça
      pra rodar o script durante a defesa.
