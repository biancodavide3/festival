from flask import Flask
from login import login_manager
from routes.auth_routes import auth_bp
from routes.public_routes import public_bp
from routes.private_routes import private_bp

import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "Chiave segretissima"

# il login manager e' configurato nel suo file apposito "login.py"

login_manager.init_app(app)

# 3 blueprint per pagine relative a autenticazione (login, signup),
# pagine pubbliche (home, performance...)
# pagine private (aree riservate per organizzatori e partecipanti)

app.register_blueprint(auth_bp)
app.register_blueprint(public_bp)
app.register_blueprint(private_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
