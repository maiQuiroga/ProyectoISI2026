# Plataforma Colaborativa de Preguntas y Respuestas (Q&A)

Proyecto integrador de Ingeniería de Software desarrollado en Python con Flask, orientado a estudiantes universitarios y preparado para respuestas asistidas por múltiples modelos de IA mediante el patrón Strategy.

<!-- Requisitos previos -->

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) instalado


<!-- Configuración del entorno local -->

1.Clonar el repositorio y entrar al directorio

2.Sincronizar dependencias y entorno virtual: uv sync

3.Configurar variables de entorno: cp.env.example .env

4.Levantar la aplicacion localmente: uv run flask --app qa_app:create_app run --debug

(localhost:500/health)

5.Calidad de codigo y tests: uv run ruff check .

