import sys
from datetime import datetime
from pathlib import Path
from guardian.agent import generar_tests
from guardian.sandbox import ejecutar_en_sandbox


def _generar_reporte_md(resultado: dict, ruta_engine: str) -> None:
    total = resultado["passed"] + resultado["failed"]
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    lineas = [
        "# Reporte Final · Quality Guardian · Nómina Pro",
        "",
        f"**Fecha:** {fecha}",
        f"**Archivo auditado:** `{ruta_engine}`",
        "",
        "---",
        "",
        f"## Veredicto: {resultado['veredicto']}",
        "",
        "| Casos ejecutados | Casos pasados | Bugs detectados |",
        "|---|---|---|",
        f"| {total} | {resultado['passed']} | {resultado['bugs_detectados']} |",
        "",
        "---",
        "",
        "## Detalle de casos de prueba",
        "",
        "| # | Test | Estado | Duración (s) |",
        "|---|---|---|---|",
    ]

    for i, t in enumerate(resultado.get("detalle_tests", []), start=1):
        estado = "✅ PASÓ" if t["outcome"] == "passed" else "❌ FALLÓ"
        nombre = t["nombre"].replace("test_generated.py::", "")
        lineas.append(f"| {i} | `{nombre}` | {estado} | {t['duracion']} |")

    lineas.append("")

    if resultado.get("mensajes_error"):
        lineas += ["## Bugs encontrados", ""]
        for msg in resultado["mensajes_error"]:
            lineas.append(f"- `{msg}`")
        lineas.append("")

    lineas += [
        "---",
        "",
        "_Reporte generado automáticamente por el Quality Guardian._",
    ]

    Path("reporte_final.md").write_text("\n".join(lineas), encoding="utf-8")
    print("[guardian] reporte_final.md generado.")


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python guardian.py src/engine.py")
        sys.exit(1)

    ruta_engine = sys.argv[1]

    print("=" * 50)
    print("  QUALITY GUARDIAN · Nómina Pro")
    print("=" * 50)

    generar_tests(ruta_engine)
    resultado = ejecutar_en_sandbox()

    print()
    print("=" * 50)
    print("  REPORTE FINAL · QUALITY GUARDIAN")
    print("=" * 50)
    print(f"  Veredicto      : {resultado['veredicto']}")
    print(f"  Casos pasados  : {resultado['passed']}")
    print(f"  Bugs detectados: {resultado['bugs_detectados']}")
    if resultado.get("mensajes_error"):
        print("  Detalle de bugs:")
        for msg in resultado["mensajes_error"]:
            print(f"    · {msg}")
    print("=" * 50)

    _generar_reporte_md(resultado, ruta_engine)


if __name__ == "__main__":
    main()
