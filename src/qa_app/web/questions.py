from datetime import UTC, datetime

from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)

questions_bp = Blueprint("questions", __name__)


def _questions_store():
    return current_app.extensions["qa_questions"]


def _timestamp():
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")


def _find_question(question_id):
    return next(
        (
            question
            for question in _questions_store()["items"]
            if question["id"] == question_id
        ),
        None,
    )


@questions_bp.get("/")
def index():
    return render_template(
        "questions/index.html", questions=_questions_store()["items"]
    )


@questions_bp.post("/questions")
def create():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    body = request.form.get("body", "").strip()
    tags = [
        tag.strip() for tag in request.form.get("tags", "").split(",") if tag.strip()
    ]

    if not title or not category or not body:
        abort(400, description="El título, la categoría y el detalle son obligatorios.")

    store = _questions_store()
    question_id = store["next_id"]
    store["next_id"] += 1
    store["items"].append(
        {
            "id": question_id,
            "title": title,
            "category": category,
            "tags": tags,
            "body": body,
            "created_at": _timestamp(),
            "responses": [],
        }
    )
    return redirect(url_for("questions.detail", question_id=question_id))


@questions_bp.get("/questions/<int:question_id>")
def detail(question_id):
    question = _find_question(question_id)
    if question is None:
        abort(404)
    return render_template(
        "questions/detail.html",
        question=question,
        responses=question["responses"],
    )


@questions_bp.post("/questions/<int:question_id>/responses")
def add_response(question_id):
    question = _find_question(question_id)
    if question is None:
        abort(404)

    body = request.form.get("body", "").strip()
    if not body:
        abort(400, description="La respuesta no puede estar vacía.")

    question["responses"].append(
        {
            "author_name": "Usuario",
            "body": body,
            "is_ai": False,
            "is_accepted": False,
            "created_at": _timestamp(),
        }
    )
    return redirect(url_for("questions.detail", question_id=question_id))
