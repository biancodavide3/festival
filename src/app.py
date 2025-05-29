from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from dao import biglietti_dao, performances_dao, utenti_dao

app = Flask(__name__)
app.config["SECRET_KEY"] = "Chiave segretissima"
login_manager = LoginManager()
login_manager.init_app(app)

# convenzione: utente si riferisce all'entita' del database, user all'oggetto di flask-login
# codice qui sotto suddiviso in 4 sezioni: 1. login manager, 2. routes flask login,
# 3. routes pubbliche, 4. routes aree personali

# 1. login manager

class User(UserMixin):
    def __init__(self, id, nome, cognome, email, password, ruolo):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password
        self.ruolo = ruolo

@login_manager.user_loader
def load_user(id):
    utente = utenti_dao.get_utente_by_id(id)
    if utente is None:
        return None
    user = User(
            id=utente["id"],
            nome=utente["nome"],
            cognome=utente["cognome"],
            email=utente["email"],
            password=utente["password"],
            ruolo=utente["ruolo"]
        )
    return user

# 2. routes flask login

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    nome = request.form.get("nome")
    cognome = request.form.get("cognome")
    email = request.form.get("email")
    if "@" not in email:
        flash("Email non valida", "error")
        return redirect(url_for("signup"))
    if utenti_dao.get_utente_by_email(email):
        flash("Email gia' utilizzata", "error")
        return redirect(url_for("signup"))
    password = request.form.get("password")
    if len(password) < 8:
        flash("Password troppo corta", "error")
        return redirect(url_for("signup"))
    password_hash = generate_password_hash(password)
    ruolo = request.form.get("ruolo")
    if ruolo not in ("organizzatore", "partecipante"):
        flash("Ruolo non valido", "error")
        return redirect(url_for("signup"))
    utenti_dao.add_utente(nome, cognome, email, password_hash, ruolo)
    return redirect(url_for("home"))


@app.route("/authenticate", methods=["POST"])
def authenticate():
    email = request.form.get("email")
    password = request.form.get("password")
    utente = utenti_dao.get_utente_by_email(email)
    if not utente or not check_password_hash(utente["password"], password):
        flash("Credenziali non valide", "error")
        return redirect(url_for("login"))
    new = User(
        id=utente["id"],
        nome=utente["nome"],
        cognome=utente["cognome"],
        email=utente["email"],
        password=utente["password"],
        ruolo=utente["ruolo"]
    )
    login_user(new)
    flash("Login effettuato con successo!", "success")
    return redirect(url_for("home"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout effettuato con successo!", "success")
    return redirect(url_for("home"))

# 3. routes pubbliche

@app.route("/")
def home():
    return render_template("home.html")

# 4.routes aree personali
# ...

