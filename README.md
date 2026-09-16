# Case FP&A Agêntico — o agente que conta a história dos números

Redesenho de um agente de IA que gera narrativas executivas mensais de
margem, para um case técnico de processo seletivo. Detalhes completos do
formato de entrega e o mapeamento de cada exigência para o que foi
entregue: **[ENTREGA.md](ENTREGA.md)**.

## Entrega — acesso rápido

| O quê | Onde |
|---|---|
| 📄 Documento avaliado (.md + anexo de processo) | [`motor-fpa/case_vertice_fpa.md`](motor-fpa/case_vertice_fpa.md) |
| 🌐 Protótipo interativo, ao vivo, sem instalar nada | **https://mrodrigues05.github.io/fpa-narrative-agent-redesign/** |
| 💻 Código-fonte completo | **https://github.com/mrodrigues05/fpa-narrative-agent-redesign** |
| 🧾 O que foi pedido × o que foi entregue, com links | [`ENTREGA.md`](ENTREGA.md) |

O restante deste documento é operacional: como rodar tudo localmente, do
zero, sem depender de nada além do que está descrito aqui.

## 1. O que cada arquivo faz

| Arquivo | Papel |
|---|---|
| `motor-fpa/case_vertice_fpa.md` | O documento avaliado — avaliação das narrativas, causa raiz, redesenho, riscos, anexo de processo. |
| `motor-fpa/margem.xlsx` | A fonte de dados. Abas "Garantia" e "Consignado" com os drivers brutos; a linha de margem é **fórmula**, não valor colado. |
| `motor-fpa/agent_engine.py` | O motor determinístico em Python: lê `margem.xlsx`, recalcula a margem, monta a evidência, testa a hipótese histórica e roda o checker. |
| `motor-fpa/agente_fpa_landing.html` | A demonstração interativa do mesmo motor, em JavaScript, com painel "Execução do Agente". |
| `motor-fpa/sync_landing_data.py` | Regrava os dados embutidos da landing page a partir de `margem.xlsx`, pra nunca ficarem dessincronizados. |
| `motor-fpa/rodar_tudo.py` | Roda o motor, sincroniza a landing page e abre ela no navegador — os três passos abaixo numa só chamada. |

Todos já vêm prontos. Este documento é sobre como colocá-los pra rodar.

## 2. Preparar o ambiente

Você precisa de **Python 3.9 ou mais recente**. Verifique:

```bash
python --version
```

No Windows, se `python3` (com o "3") não for reconhecido mas `python` funcionar,
use `python` — é só o alias da Microsoft Store no lugar do interpretador de
verdade; não afeta em nada o resultado.

O único pacote externo usado é o `openpyxl` (lê o `.xlsx`). Se o comando abaixo
der erro de import, instale:

```bash
pip install openpyxl
```

Nenhum outro pacote, chave de API, ou serviço externo é necessário para rodar
o script Python. Para a landing page, basta um navegador — não precisa de
servidor, Node, nem instalação de nada.

## 3. Rodar tudo de uma vez (recomendado)

```bash
cd motor-fpa
python rodar_tudo.py
```

Isso roda o motor em terminal, sincroniza a landing page com `margem.xlsx` e
já abre a página no navegador padrão. Os passos 4 e 5 abaixo explicam cada
parte separadamente, caso você precise rodar só uma delas.

## 4. Rodar o motor (prova em terminal)

Dentro de `motor-fpa/`:

```bash
python agent_engine.py
```

Saída esperada (resumo): os três casos (A, B, C) imprimem a evidência
recalculada, o status da hipótese histórica, a narrativa e o resultado do
checker, terminando em:

```
OK — hipótese confirmada em A, contradita em B, driver correto identificado,
     e evidência ambígua do Caso C não vira um driver inventado.
```

Pra analisar qualquer outro par de meses presente na planilha (por exemplo,
depois de adicionar novos meses a `margem.xlsx`), sem editar o código:

```bash
python agent_engine.py <mes_atual> <mes_comparacao>
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
| `FileNotFoundError: DADO AUSENTE: não encontrei '.../margem.xlsx'` | O script não achou a planilha na mesma pasta. | Confira se `margem.xlsx` está dentro de `motor-fpa/`. |
| `ValueError: DADO AUSENTE: driver 'X' não encontrado` | Uma linha da planilha foi renomeada ou apagada. | Confira se os rótulos da coluna A da aba continuam com as palavras-chave esperadas (ex.: "taxa", "funding", "cac"...). |
| `ModuleNotFoundError: No module named 'openpyxl'` | Pacote não instalado. | `pip install openpyxl`. |

## 5. Abrir a landing page

Depois de rodar `python sync_landing_data.py` pelo menos uma vez (ou
`rodar_tudo.py`, que já faz isso), dê duplo clique em
`motor-fpa/agente_fpa_landing.html` — ele abre em qualquer navegador, sem
instalar nada e sem depender de internet. Todo o motor roda no seu próprio
navegador (JavaScript puro) e a narrativa vem de um template determinístico —
não há nenhuma chamada de API, então não há custo nem dependência de rede.

### Mantendo a landing page sincronizada com margem.xlsx

Os números que a página usa por padrão (sem upload) ficam num bloco marcado
dentro do `<script>`, gerado automaticamente — não edite esse bloco à mão.
Toda vez que `margem.xlsx` mudar, rode:

```bash
python sync_landing_data.py
```

Isso regrava o bloco a partir da planilha, então a página nunca fica com
números diferentes do `margem.xlsx` por esquecimento.

### Usando o painel "Execução do Agente"

1. Escolha **Período atual** e **Comparação** (o par de meses a analisar).
2. Escolha **Contexto**: `v1.0` reproduz o agente antigo (regra fixa, sempre
   cita mix); `v2.0` é o redesenho (testa a hipótese contra o dado atual).
3. Clique **▶ Executar análise**, ou **⚡ Run Adversarial Test** pra já rodar
   direto o caso crítico (agosto vs. julho) com o contexto v2.0.
4. Acompanhe o pipeline rodando passo a passo, abra o prompt em execução (ele
   monta o SYSTEM + CONTEXT + EVIDENCE + TASK completo, só não envia a
   nenhuma API), e confira o resultado em Evidências → Narrativa → Validação.

### Carregando uma planilha diferente na hora

No topo do painel Agent Run tem um campo "Fonte de dados". Sem nada
selecionado, a página usa os números sincronizados de `margem.xlsx`. Se você
carregar um `.xlsx` no mesmo formato (abas "Garantia" e "Consignado", mesmos
rótulos de driver), a página substitui os dados só naquela sessão do
navegador (sem alterar o arquivo) e os seletores de mês se atualizam
sozinhos.

## 6. Checklist antes da apresentação

- [ ] `python motor-fpa/rodar_tudo.py` roda sem erro, termina em "OK" no
      terminal e abre a landing page já sincronizada.
- [ ] `agente_fpa_landing.html` abre (duplo clique, qualquer navegador) e o
      botão "⚡ Run Adversarial Test" mostra o painel de rejeição da hipótese
      histórica.
- [ ] `margem.xlsx` está dentro de `motor-fpa/`, caso alguém peça pra rodar o
      script durante a defesa.
