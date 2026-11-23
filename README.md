# Plataforma Colaborativa de Preguntas y Respuestas (Q&A)

Proyecto integrador de Ingeniería de Software desarrollado en Python con Flask, orientado a estudiantes universitarios y preparado para respuestas asistidas por múltiples modelos de IA mediante el patrón Strategy.

<!-- Requisitos previos -->

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) instalado


<!-- Configuración del entorno local -->

1. Descargar o clonar el repositorio y abrir una terminal dentro de la carpeta `ProyectoISI2026`.

2. Instalar las dependencias y preparar el entorno virtual:

	uv sync

3. Crear las tablas de la base de datos local:

	uv run alembic upgrade head

	La aplicación usa SQLite y crea la base en `instance/qa_app.db`. No es necesario configurar una base de datos para probarla.

4. Iniciar la aplicación:

	uv run flask --app qa_app:create_app run --debug

5. Abrir la aplicación en el navegador:

	`http://127.0.0.1:5000`

	Para comprobar que el servidor está activo, abrir `http://127.0.0.1:5000/health`. Debe mostrar `{"status":"ok"}`.

6. Probar el flujo Q&A:

	- Publicar una pregunta y abrir su detalle desde el listado.
	- En el detalle, enviar una respuesta y comprobar que aparece en la página.
	- Para probar la respuesta automática simulada, publicar una pregunta con la etiqueta `ia-help`.

7. Dar el rol Admin a una cuenta:

	Primero registra la cuenta desde la aplicación. Luego, en otra terminal abierta en la carpeta del proyecto, ejecuta el comando con el correo de esa cuenta:

	uv run flask --app qa_app:create_app create-admin usuario@example.com

	El comando promueve a Admin la cuenta que ya existe y conserva su contraseña. Si el correo todavía no está registrado, crea una cuenta nueva y solicita nombre y contraseña.

8. Ejecutar las pruebas (opcional):

	uv run pytest

9. Revisar el estilo del código (opcional):

	uv run ruff check .

