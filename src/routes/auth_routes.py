from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from dao import utenti_dao
from login import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signup")
def signup():
    return render_template("auth/signup.html")

@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout effettuato con successo!", "info")
    return redirect(url_for("public.home"))

# ---------- form actions ------------------------

@auth_bp.route("/subscribe", methods=["POST"])
def subscribe():
    nome = request.form.get("nome")
    if not nome:
        flash("Inserisci un nome valido", "danger")
        return redirect(url_for("auth.signup"))
    cognome = request.form.get("cognome")
    if not cognome:
        flash("Inserisci un cognome valido", "danger")
    email = request.form.get("email")
    if not email or "@" not in email:
        flash("Email non valida", "danger")
        return redirect(url_for("auth.signup"))
    if utenti_dao.get_utente_by_email(email):
        flash("Email già utilizzata", "danger")
        return redirect(url_for("auth.signup"))
    password = request.form.get("password")
    if len(password) < 8:
        flash("La password deve contenere almeno 8 caratteri", "danger")
        return redirect(url_for("auth.signup"))
    password_hash = generate_password_hash(password, method="scrypt")
    ruolo = request.form.get("ruolo")
    if ruolo not in ("organizzatore", "partecipante"):
        flash("Ruolo non valido", "danger")
        return redirect(url_for("auth.signup"))
    id = utenti_dao.add_utente(nome, cognome, email, password_hash, ruolo)
    user = User(
        id=id,
        nome=nome,
        cognome=cognome,
        email=email,
        password=password_hash,
        ruolo=ruolo
    )
    login_user(user)
    flash("Registrazione effettuata con successo!", "success")
    return redirect(url_for("private.reserved"))

@auth_bp.route("/authenticate", methods=["POST"])
def authenticate():
    email = request.form.get("email")
    if not email or "@" not in email:
        flash("Email non valida", "danger")
        return redirect(url_for("auth.login")) 
    password = request.form.get("password")
    if not password:
        flash("Inserisci la password", "danger")
        return redirect(url_for("auth.login"))
    utente = utenti_dao.get_utente_by_email(email)
    if not utente or not check_password_hash(utente["password"], password):
        flash("Credenziali non valide", "danger")
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
    return redirect(url_for("private.reserved"))


