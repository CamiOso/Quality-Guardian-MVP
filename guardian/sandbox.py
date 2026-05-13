import subprocess
import json
from pathlib import Path


def ejecutar_en_sandbox() -> dict:
    """Corre pytest dentro del contenedor Docker y retorna el veredicto."""

    print("[sandbox] iniciando contenedor guardian-sandbox...")

    resultado = subprocess.run(
        [
            "docker", "run", "--rm",
            "-v", f"{Path.cwd()}:/app",
            "-w", "/app",
            "guardian-sandbox",
            "pytest", "test_generated.py",
            "--json-report",
            "--json-report-file=.report.json",
            "-v",
        ],
        capture_output=True,
        text=True,
    )

    print(resultado.stdout)

    reporte_path = Path(".report.json")
    if not reporte_path.exists():
        print("[sandbox] ERROR: no se generó .report.json")
        return {"passed": 0, "failed": 0, "veredicto": "ERROR", "bugs_detectados": 0}

    reporte = json.loads(reporte_path.read_text(encoding="utf-8"))
    passed = reporte["summary"].get("passed", 0)
    failed = reporte["summary"].get("failed", 0)

    print(f"[sandbox] resultados: {passed} passed · {failed} failed")

    return {
        "passed": passed,
        "failed": failed,
        "bugs_detectados": failed,
        "veredicto": "APROBADO" if failed == 0 else "RECHAZADO",
    }
