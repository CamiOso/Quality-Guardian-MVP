from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
import re


def generar_tests(ruta_engine: str, ruta_casos: str = "docs/casos_prueba.md") -> None:
    """Lee engine.py y casos_prueba.md, genera test_generated.py con pytest."""

    ruta_engine = Path(ruta_engine)
    ruta_casos = Path(ruta_casos)

    print(f"[agent] leyendo {ruta_engine}...")
    codigo = ruta_engine.read_text(encoding="utf-8")

    if ruta_casos.exists():
        print(f"[agent] leyendo {ruta_casos}...")
        casos = ruta_casos.read_text(encoding="utf-8")
    else:
        print("[agent] casos_prueba.md no encontrado, usando casos genéricos...")
        casos = "Generar casos de prueba básicos cubriendo happy path, bordes y errores."

    print("[agent] conectando con llama3:8b via Ollama...")
    llm = OllamaLLM(model="llama3:8b")

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

    # Limpia bloques markdown si el modelo los incluye
    codigo_limpio = re.sub(r"```(?:python)?|```", "", resultado).strip()

    Path("test_generated.py").write_text(codigo_limpio, encoding="utf-8")
    print("[agent] test_generated.py listo.")
