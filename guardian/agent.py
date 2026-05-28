import os
from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
import re


def _crear_llm():
    groq_key = os.environ.get("GROQ_API_KEY")
    ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

    if groq_key:
        print("[agent] usando Groq API (llama3-8b-8192)...")
        return ChatGroq(model="llama-3.1-8b-instant", api_key=groq_key)

    print(f"[agent] usando Ollama local en {ollama_url}...")
    return OllamaLLM(
        model="llama3.1:8b",
        base_url=ollama_url,
        num_ctx=2048,
        num_predict=900,
        num_thread=2,
        num_batch=64,
    )


def _resumir_casos(texto: str) -> str:
    """Extrae título, entrada, salida esperada y regla de cada caso."""
    lineas_utiles = []
    for linea in texto.splitlines():
        s = linea.strip()
        if s.startswith(("## CP-", "**Entrada:**", "**Salida esperada:**", "**Regla:**", "-")):
            lineas_utiles.append(s)
    return "\n".join(lineas_utiles)


def generar_tests(ruta_engine: str, ruta_casos: str = "docs/casos_prueba.md") -> None:
    """Lee engine.py y casos_prueba.md, genera test_generated.py con pytest."""

    ruta_engine = Path(ruta_engine)
    ruta_casos = Path(ruta_casos)

    print(f"[agent] leyendo {ruta_engine}...")
    codigo = ruta_engine.read_text(encoding="utf-8")

    if ruta_casos.exists():
        print(f"[agent] leyendo {ruta_casos}...")
        casos = _resumir_casos(ruta_casos.read_text(encoding="utf-8"))
    else:
        print("[agent] casos_prueba.md no encontrado, usando casos genéricos...")
        casos = "Generar casos de prueba básicos cubriendo happy path, bordes y errores."

    llm = _crear_llm()

    # Deriva el módulo de import a partir de la ruta del archivo auditado
    # Ej: src/engine_buggy.py -> from src.engine_buggy import liquidar_nomina
    modulo_import = str(ruta_engine).replace("/", ".").removesuffix(".py")

    prompt = ChatPromptTemplate.from_template("""
Eres un QA Engineer experto en Python. Analiza el siguiente código:

```python
{codigo}
```

Y los siguientes casos de prueba definidos por el equipo:

{casos}

Tu tarea:
1. Genera un archivo de pruebas completo usando pytest.
2. REGLA CRÍTICA: Todas las funciones DEBEN empezar con "test_" (ejemplo: def test_cp01_...).
3. REGLA CRÍTICA: Las funciones NO deben tener parámetros. Solo def test_nombre(): sin nada adentro de los paréntesis.
4. Usa EXACTAMENTE los valores de entrada y salida esperada de cada caso. No inventes valores.
5. El salario_base mínimo válido es 1_300_000. Nunca uses valores menores en tests que no esperan excepción.
6. Los parámetros se llaman: salario_base, horas_extras_diurnas, horas_extras_nocturnas, vlr_hora.
7. REGLA CRÍTICA: El import DEBE ser exactamente: from {modulo_import} import liquidar_nomina
8. Usa pytest.raises para los casos que esperan excepciones (ValueError o ErrorNomina).
9. No agregues pytest.main() ni ninguna línea al final del archivo.
10. Devuelve SOLO el código Python, sin explicaciones ni bloques markdown.
""")

    print("[agent] generando test_generated.py...")
    cadena = prompt | llm
    resultado = cadena.invoke({"codigo": codigo, "casos": casos, "modulo_import": modulo_import})

    # ChatGroq devuelve AIMessage, OllamaLLM devuelve str
    texto = resultado.content if hasattr(resultado, "content") else resultado

    # Quita bloques markdown
    texto = re.sub(r"```(?:python)?|```", "", texto)

    # Arranca desde el primer import/from para descartar cualquier
    # cabecera ini-style o comentarios de ruta que el LLM añade antes del código
    lineas = texto.splitlines()
    inicio = next(
        (i for i, l in enumerate(lineas) if l.strip().startswith(("import ", "from "))),
        0,
    )

    codigo_limpio = "\n".join(lineas[inicio:]).strip()

    # Elimina líneas finales que no sean Python válido (frases del LLM)
    import ast
    lineas_codigo = codigo_limpio.splitlines()
    while lineas_codigo:
        try:
            ast.parse("\n".join(lineas_codigo))
            break
        except SyntaxError:
            lineas_codigo.pop()
    codigo_limpio = "\n".join(lineas_codigo).strip()

    Path("test_generated.py").write_text(codigo_limpio, encoding="utf-8")
    print("[agent] test_generated.py listo.")
