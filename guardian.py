import sys
from guardian.agent import generar_tests
from guardian.sandbox import ejecutar_en_sandbox


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


if __name__ == "__main__":
    main()
