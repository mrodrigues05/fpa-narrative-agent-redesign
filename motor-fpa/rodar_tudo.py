"""
Roda a demonstração completa numa tacada só:
  1) o motor determinístico em terminal (agent_engine.py, Casos A/B/C + regressão)
  2) sincroniza a landing page com margem.xlsx (sync_landing_data.py)
  3) abre a landing page no navegador padrão

Uso:
    python rodar_tudo.py
"""
import subprocess
import sys
import webbrowser
from pathlib import Path

PASTA = Path(__file__).parent


def rodar(script):
    print(f"\n{'=' * 60}\n{script}\n{'=' * 60}", flush=True)
    subprocess.run([sys.executable, str(PASTA / script)], check=True, cwd=PASTA)


def main():
    rodar("agent_engine.py")
    rodar("sync_landing_data.py")

    landing = PASTA / "agente_fpa_landing.html"
    print(f"\nAbrindo {landing.name} no navegador padrão...")
    webbrowser.open(landing.resolve().as_uri())


if __name__ == "__main__":
    main()
