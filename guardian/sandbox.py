import subprocess
import shutil
import sys
import json
from pathlib import Path


def _extraer_mensajes_error(reporte: dict) -> list[str]:
    mensajes = []
    for test in reporte.get("tests", []):
        if test.get("outcome") == "failed":
            nombre = test.get("nodeid", "test desconocido")
            call = test.get("call", {})
            longrepr = call.get("longrepr", "sin detalle")
            linea_error = longrepr.strip().splitlines()[-1] if longrepr else "sin detalle"
            mensajes.append(f"{nombre}: {linea_error}")
    return mensajes


def _extraer_detalle_tests(reporte: dict) -> list[dict]:
    detalle = []
    for test in reporte.get("tests", []):
        nombre = test.get("nodeid", "desconocido")
        outcome = test.get("outcome", "unknown")
        duracion = round(test.get("call", {}).get("duration", 0), 4)
        call = test.get("call", {})
        longrepr = call.get("longrepr", "")
        linea_error = longrepr.strip().splitlines()[-1] if longrepr and outcome == "failed" else ""
        detalle.append({
            "nombre": nombre,
            "outcome": outcome,
            "duracion": duracion,
            "error": linea_error,
        })
    return detalle


def ejecutar_en_sandbox() -> dict:
    """Corre pytest en Docker (o localmente si Docker no está disponible)."""

    docker_bin = shutil.which("docker")
    usar_docker = docker_bin is not None and subprocess.run(
        ["docker", "info"], capture_output=True
    ).returncode == 0

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
    detalle_tests = _extraer_detalle_tests(reporte)

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
        "detalle_tests": detalle_tests,
    }
