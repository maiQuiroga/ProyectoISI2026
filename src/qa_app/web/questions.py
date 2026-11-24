from types import SimpleNamespace

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import select

from qa_app.extensions import db
from qa_app.models import Answer, Category, Question, RoleType, Tag
from qa_app.services.ai_strategies import geminiStrategy
from qa_app.services.auto_response_service import (
    AutoResponseService,
    process_unanswered_questions,
)
from qa_app.web.auth import get_current_user

questions_bp = Blueprint("questions", __name__)
VALID_CATEGORIES = {"Python", "Flask", "Base de Datos", "Diseño / UML"}


def _require_login():
    user = get_current_user()
    if user is None:
        flash("Inicia sesión para publicar preguntas o respuestas.", "error")
        return None
    return user


def _answer_view(answer):
    return SimpleNamespace(
        author_name=answer.author.name,
        body=answer.body,
        is_ai=answer.author.type == "AiAgente",
        is_accepted=answer.is_accepted,
        created_at=answer.publication_date.strftime("%Y-%m-%d"),
    )


def _question_view(question):
    return SimpleNamespace(
        id=question.id,
        title=question.title,
        category=question.category.name,
        tags=[tag.name for tag in question.tags],
        body=question.body,
        created_at=question.publication_date.strftime("%Y-%m-%d"),
        responses=[_answer_view(answer) for answer in question.answers],
    )


@questions_bp.get("/")
def index():
    process_unanswered_questions(db.session)
    questions = db.session.scalars(
        select(Question).order_by(Question.publication_date.desc(), Question.id)
    ).all()
    return render_template(
        "questions/index.html",
        questions=[_question_view(question) for question in questions],
    )


@questions_bp.post("/questions")
def create():
    author = _require_login()
    if author is None:
        return redirect(url_for("auth.login"))

    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    body = request.form.get("body", "").strip()
    tags = [
        tag.strip() for tag in request.form.get("tags", "").split(",") if tag.strip()
    ]

    if not title or not body or category not in VALID_CATEGORIES:
        abort(400, description="El título, la categoría y el detalle son obligatorios.")
    if len(title) > 200 or any(len(tag) > 50 for tag in tags):
        abort(
            400, description="El título o alguna etiqueta supera el límite permitido."
        )

    category_model = db.session.scalar(
        select(Category).where(Category.name == category)
    )
    if category_model is None:
        category_model = Category(name=category)
        db.session.add(category_model)

    tag_models = []
    for tag_name in dict.fromkeys(tag.lstrip("#") for tag in tags):
        tag_model = db.session.scalar(select(Tag).where(Tag.name == tag_name))
        if tag_model is None:
            tag_model = Tag(name=tag_name)
            db.session.add(tag_model)
        tag_models.append(tag_model)

    question = Question(
        title=title,
        body=body,
        author=author,
        category=category_model,
        tags=tag_models,
    )
    db.session.add(question)
    db.session.flush()

    service = AutoResponseService(strategy=geminiStrategy())
    auto_response = service.generate_for_question(question)  
    if auto_response is not None:
        db.session.add(auto_response)

    db.session.commit()
    return redirect(url_for("questions.detail", question_id=question.id))


@questions_bp.get("/questions/<question_id>")
def detail(question_id):
    question = db.session.get(Question, question_id)
    if question is None:
        abort(404)
    return render_template(
        "questions/detail.html",
        question=_question_view(question),
        responses=[_answer_view(answer) for answer in question.answers],
    )


@questions_bp.post("/questions/<question_id>/responses")
def add_response(question_id):
    author = _require_login()
    if author is None:
        return redirect(url_for("auth.login"))

    question = db.session.get(Question, question_id)
    if question is None:
        abort(404)

    body = request.form.get("body", "").strip()
    if not body:
        abort(400, description="La respuesta no puede estar vacía.")

    answer = Answer(body=body, author=author, question=question)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for("questions.detail", question_id=question_id))


@questions_bp.post("/questions/<question_id>/delete")
def delete_question(question_id):
    user = get_current_user()
    if user is None:
        flash("Inicia sesión para continuar.", "error")
        return redirect(url_for("auth.login"))
    if user.role != RoleType.ADMIN:
        abort(403)

    question = db.session.get(Question, question_id)
    if question is None:
        abort(404)

    db.session.delete(question)
    db.session.commit()
    flash("La pregunta fue eliminada.", "success")
    return redirect(url_for("questions.index"))
