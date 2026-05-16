import subprocess
import shutil
import sys
import json
from pathlib import Path


def _extraer_mensajes_error(reporte: dict) -> list[str]:
    """Extrae los mensajes de error de cada test fallido del reporte JSON."""
    mensajes = []
    for test in reporte.get("tests", []):
        if test.get("outcome") == "failed":
            nombre = test.get("nodeid", "test desconocido")
            call = test.get("call", {})
            longrepr = call.get("longrepr", "sin detalle")
            # Tomar solo la última línea (el AssertionError o mensaje concreto)
            linea_error = longrepr.strip().splitlines()[-1] if longrepr else "sin detalle"
            mensajes.append(f"{nombre}: {linea_error}")
    return mensajes


def ejecutar_en_sandbox() -> dict:
    """Corre pytest en Docker (o localmente si Docker no está disponible)."""

    usar_docker = shutil.which("docker") is not None

    if usar_docker:
        print("[sandbox] iniciando contenedor guardian-sandbox...")
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path.cwd()}:/app",
            "-w", "/app",
            "guardian-sandbox",
            "pytest", "test_generated.py",
            "--json-report",
            "--json-report-file=.report.json",
            "-v",
        ]
    else:
        print("[sandbox] Docker no disponible, ejecutando pytest localmente...")
        cmd = [
            sys.executable, "-m", "pytest", "test_generated.py",
            "--json-report",
            "--json-report-file=.report.json",
            "-v",
        ]

    resultado = subprocess.run(cmd, capture_output=True, text=True)

    print(resultado.stdout)

    reporte_path = Path(".report.json")
    if not reporte_path.exists():
        print("[sandbox] ERROR: no se generó .report.json")
        return {
            "passed": 0,
            "failed": 0,
            "veredicto": "ERROR",
            "bugs_detectados": 0,
            "mensajes_error": [],
        }

    reporte = json.loads(reporte_path.read_text(encoding="utf-8"))
    passed = reporte["summary"].get("passed", 0)
    failed = reporte["summary"].get("failed", 0)
    mensajes_error = _extraer_mensajes_error(reporte)

    print(f"[sandbox] resultados: {passed} passed · {failed} failed")
    if mensajes_error:
        print("[sandbox] bugs detectados:")
        for msg in mensajes_error:
            print(f"  · {msg}")

    return {
        "passed": passed,
        "failed": failed,
        "bugs_detectados": failed,
        "veredicto": "APROBADO" if failed == 0 else "RECHAZADO CON BUGS",
        "mensajes_error": mensajes_error,
    }
