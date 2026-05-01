# Quality Guardian MVP

> De pedirle código a una IA, a construir un agente autónomo que analiza, prueba y encuentra fallos lógicos.

Un agente de IA agéntica que recibe código Python, lo analiza, genera pruebas y las ejecuta en un sandbox aislado para detectar bugs de forma autónoma.

---

## ¿Qué es este proyecto?

**Quality Guardian** es el proyecto central del taller COIL entre la Universidad de Caldas (UdeC) y la Universidad Metropolitana de Bucaramanga (UMB). Ocho células mixtas de estudiantes construyen un agente que:

1. Recibe un archivo `.py` como input
2. Analiza el código usando un LLM local (Llama 3 vía Ollama)
3. Genera automáticamente un script de pruebas con LangChain
4. Ejecuta las pruebas dentro de un contenedor Docker
5. Emite un veredicto: `APROBADO` o `RECHAZADO CON BUGS`

---

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| LLM local | Llama 3 8B vía [Ollama](https://ollama.com) |
| Orquestación | [LangChain](https://www.langchain.com) / CrewAI |
| Lenguaje | Python 3.11+ |
| Testing | Pytest + pytest-json-report |
| Sandbox | Docker |

Todo el stack es **100% open source** y corre localmente. Sin APIs de pago.

---

## Estructura del proyecto

```
quality-guardian-mvp/
├── src/
│   └── engine.py           # Algoritmo a auditar (entrega UdeC)
├── guardian/
│   ├── agent.py            # Agente LangChain (análisis + generación)
│   └── sandbox.py          # Ejecución en Docker
├── docs/
│   └── casos_prueba.md     # Matriz de casos de prueba
├── test_generated.py       # Generado automáticamente por el agente
├── Dockerfile              # Sandbox de pruebas aislado
└── README.md
```

---

*Universidad de Caldas × Universidad Metropolitana de Bucaramanga · 2026*
