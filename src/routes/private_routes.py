from flask import Blueprint, render_template
from flask_login import current_user, login_required

private_bp = Blueprint('private', __name__)

@private_bp.route("/reserved")
@login_required
def reserved():
    if current_user.ruolo == "organizzatore":
        return render_template("private/riservata_organizzatori.html", user=current_user)
    return render_template("private/riservata_partecipanti.html", user=current_user)
