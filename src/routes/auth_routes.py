from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from dao import utenti_dao

auth_bp = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, id, nome, cognome, email, password, ruolo):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password
        self.ruolo = ruolo

from app import login_manager

@login_manager.user_loader
def load_user(id):
    utente = utenti_dao.get_utente_by_id(id)
    if utente is None:
        return None
    return User(
        id=utente["id"],
        nome=utente["nome"],
        cognome=utente["cognome"],
        email=utente["email"],
        password=utente["password"],
        ruolo=utente["ruolo"]
    )

@auth_bp.route("/signup")
def signup():
    return render_template("signup.html")

@auth_bp.route("/login")
def login():
    return render_template("login.html")

@auth_bp.route("/subscribe", methods=["POST"])
def subscribe():
    nome = request.form.get("nome")
    cognome = request.form.get("cognome")
    email = request.form.get("email")
    if "@" not in email:
        flash("Email non valida", "error")
        return redirect(url_for("auth.signup"))
    if utenti_dao.get_utente_by_email(email):
        flash("Email già utilizzata", "error")
        return redirect(url_for("auth.signup"))
    password = request.form.get("password")
    if len(password) < 8:
        flash("Password troppo corta", "error")
        return redirect(url_for("auth.signup"))
    password_hash = generate_password_hash(password)
    ruolo = request.form.get("ruolo")
    if ruolo not in ("organizzatore", "partecipante"):
        flash("Ruolo non valido", "error")
        return redirect(url_for("auth.signup"))
    utenti_dao.add_utente(nome, cognome, email, password_hash, ruolo)
    flash("Registrazione effettuata con successo!", "success")
    return redirect(url_for("public.home"))

@auth_bp.route("/authenticate", methods=["POST"])
def authenticate():
    email = request.form.get("email")
    password = request.form.get("password")
    utente = utenti_dao.get_utente_by_email(email)
    if not utente or not check_password_hash(utente["password"], password):
        flash("Credenziali non valide", "error")
        return redirect(url_for("auth.login"))
    user = User(
        id=utente["id"],
        nome=utente["nome"],
        cognome=utente["cognome"],
        email=utente["email"],
        password=utente["password"],
        ruolo=utente["ruolo"]
    )
    login_user(user)
    flash("Login effettuato con successo!", "success")
    return redirect(url_for("public.home"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout effettuato con successo!", "success")
    return redirect(url_for("public.home"))
