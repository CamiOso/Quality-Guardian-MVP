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
        model="llama3.2:3b",
        base_url=ollama_url,
        num_ctx=2048,
        num_predict=900,
        num_thread=2,
        num_batch=64,
    )


def _resumir_casos(texto: str) -> str:
    """Extrae solo Entrada/Salida Esperada/Regla de cada caso para reducir tokens."""
    lineas_utiles = []
    for linea in texto.splitlines():
        s = linea.strip()
        if s.startswith(("### C-", "- Entrada:", "- Salida Esperada:", "- Regla Validada:")):
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

    prompt = ChatPromptTemplate.from_template("""
Eres un QA Engineer experto en Python. Analiza el siguiente código:

```python
{codigo}
```

Y los siguientes casos de prueba definidos por el equipo:

{casos}

Tu tarea:
1. Genera un archivo de pruebas completo usando pytest.
2. Cubre todos los casos de prueba listados.
3. Incluye el import correcto del módulo (from src.engine import liquidar_nomina).
4. Cada función de test debe tener un nombre descriptivo.
5. Usa pytest.raises para los casos que esperan excepciones.
6. Devuelve SOLO el código Python, sin explicaciones ni bloques markdown.
""")

    print("[agent] generando test_generated.py...")
    cadena = prompt | llm
    resultado = cadena.invoke({"codigo": codigo, "casos": casos})

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

    Path("test_generated.py").write_text(codigo_limpio, encoding="utf-8")
    print("[agent] test_generated.py listo.")
