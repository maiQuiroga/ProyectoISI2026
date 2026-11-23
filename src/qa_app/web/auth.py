from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from qa_app.extensions import db
from qa_app.models import HumanUser, RoleType

auth_bp = Blueprint("auth", __name__)


def get_current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None

    user = db.session.get(HumanUser, user_id)
    if user is None:
        session.pop("user_id", None)
    return user


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not name or not email or not password:
        flash("Todos los campos son obligatorios.", "error")
        return render_template("auth/register.html"), 400
    if len(name) > 100 or len(email) > 120:
        flash("El nombre o el correo supera la longitud permitida.", "error")
        return render_template("auth/register.html"), 400
    if len(password) < 8:
        flash("La contraseña debe tener al menos 8 caracteres.", "error")
        return render_template("auth/register.html"), 400
    if db.session.scalar(select(HumanUser).where(HumanUser.email == email)):
        flash("Ese correo ya está registrado. Inicia sesión.", "error")
        return render_template("auth/register.html"), 400

    user = HumanUser(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role=RoleType.GENERAL_USER,
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Ese correo ya está registrado. Inicia sesión.", "error")
        return render_template("auth/register.html"), 400

    session.clear()
    session["user_id"] = user.id
    flash("Tu cuenta fue creada. Ya iniciaste sesión.", "success")
    return redirect(url_for("questions.index"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    user = db.session.scalar(select(HumanUser).where(HumanUser.email == email))

    if user is None or not check_password_hash(user.password_hash, password):
        flash("Correo o contraseña incorrectos.", "error")
        return render_template("auth/login.html"), 401

    session.clear()
    session["user_id"] = user.id
    flash("Has iniciado sesión.", "success")
    return redirect(url_for("questions.index"))


@auth_bp.post("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("questions.index"))
