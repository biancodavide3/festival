from flask_login import LoginManager, UserMixin
from dao import utenti_dao

login_manager = LoginManager()

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
    return User(
        id=utente["id"],
        nome=utente["nome"],
        cognome=utente["cognome"],
        email=utente["email"],
        password=utente["password"],
        ruolo=utente["ruolo"]
    )
