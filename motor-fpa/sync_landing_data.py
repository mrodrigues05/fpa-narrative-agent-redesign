"""
Sincroniza os dados embutidos da landing page com margem.xlsx.

Antes desta automação, os números em `DRIVERS` (dentro do <script> de
agente_fpa_landing.html) tinham que ser copiados à mão do margem.xlsx toda vez
que a planilha mudava — nada garantia que os dois ficassem iguais. Este script
reaproveita o parser de agent_engine.py (mesma planilha, mesmas regras de
casamento de driver) e regrava só o bloco marcado entre
DADOS_SINCRONIZADOS_COM_MARGEM_XLSX na landing page.

Uso (depois de editar margem.xlsx e recalcular as fórmulas):
    python sync_landing_data.py
"""
import json
import re
from pathlib import Path

from agent_engine import DRIVER_ORDER, DRIVERS, EXCEL_PATH, MESES_REAIS

HTML_PATH = Path(__file__).with_name("agente_fpa_landing.html")
MARKER_START = "// >>> DADOS_SINCRONIZADOS_COM_MARGEM_XLSX (gerado por sync_landing_data.py — não edite à mão) >>>"
MARKER_END = "// <<< DADOS_SINCRONIZADOS_COM_MARGEM_XLSX <<<"


def _bu_block(bu_data, meses):
    linhas = []
    for key in DRIVER_ORDER:
        pares = ", ".join(f'"{mes}":{json.dumps(bu_data[key][mes])}' for mes in meses)
        linhas.append(f"    {key}:{' ' * max(1, 15 - len(key))}{{{pares}}},")
    return "\n".join(linhas)


def build_js_block(drivers, meses):
    meses_js = ",".join(f'"{mes}"' for mes in meses)
    return (
        f"{MARKER_START}\n"
        "// Dados de exemplo embutidos — idênticos ao margem.xlsx (abas Garantia/Consignado),\n"
        "// só para a página funcionar sem upload nem servidor. Rode `python sync_landing_data.py`\n"
        "// depois de editar margem.xlsx pra regravar este bloco automaticamente. Assim que uma\n"
        "// planilha é carregada manualmente na página, este objeto é substituído em runtime\n"
        "// pelo conteúdo do arquivo carregado (isso continua igual).\n"
        "let DRIVERS = {\n"
        "  garantia: {\n" + _bu_block(drivers["garantia"], meses) + "\n  },\n"
        "  consignado: {\n" + _bu_block(drivers["consignado"], meses) + "\n  },\n"
        "};\n"
        f"let MESES_DISPONIVEIS = [{meses_js}];\n"
        f"{MARKER_END}"
    )


def main():
    novo_bloco = build_js_block(DRIVERS, MESES_REAIS)
    html = HTML_PATH.read_text(encoding="utf-8")

    padrao = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.DOTALL)
    if not padrao.search(html):
        raise SystemExit(
            f"Não encontrei os marcadores {MARKER_START!r} em {HTML_PATH.name}. "
            "A landing page pode ter sido editada manualmente — restaure os marcadores antes de sincronizar."
        )

    html_novo = padrao.sub(lambda _: novo_bloco, html, count=1)
    if html_novo == html:
        print(f"[sync_landing_data] {HTML_PATH.name} já estava sincronizado com {EXCEL_PATH} — nada a fazer.")
    else:
        HTML_PATH.write_text(html_novo, encoding="utf-8")
        print(f"[sync_landing_data] {HTML_PATH.name} atualizado a partir de {EXCEL_PATH} — meses: {MESES_REAIS}")


if __name__ == "__main__":
    main()
