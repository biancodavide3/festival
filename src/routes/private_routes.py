from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from flask_login import current_user, login_required
from dao import biglietti_dao, performances_dao
import os
import uuid
from datetime import datetime, timedelta
import logging

private_bp = Blueprint('private', __name__)

@private_bp.route("/reserved")
@login_required
def reserved():
    biglietto = biglietti_dao.get_biglietto_by_partecipante(current_user.id)
    bozze = performances_dao.get_bozze_by_organizzatore(current_user.id)
    pubblicate = performances_dao.get_performances_pubblicate_by_organizzatore(current_user.id)
    if current_user.ruolo == "organizzatore":
        return render_template("private/riservata_organizzatori.html", user=current_user, bozze=bozze, pubblicate=pubblicate)
    return render_template("private/riservata_partecipanti.html", user=current_user, biglietto=biglietto)

# -------------------- partecipanti ------------------

@private_bp.route("/purchase", methods=["POST"])
@login_required
def compra_biglietto():
    if current_user.ruolo == "organizzatore":
        return redirect(url_for("private.reserved")) 

    tipo = request.form.get("tipo")
    giorni = request.form.getlist("giorni")

    tipi_validi = ("Biglietto Giornaliero", "Pass 2 Giorni", "Full Pass")
    giorni_validi = ("Venerdi", "Sabato", "Domenica")

    if not tipo or tipo not in tipi_validi:
        flash("Seleziona un tipo di biglietto valido", "danger")
        return redirect(url_for("private.reserved"))

    if tipo == "Full Pass":
        if set(giorni) != set(giorni_validi):
            flash("Seleziona tutti i giorni per il full pass", "danger")
            return redirect(url_for("private.reserved"))  

    elif tipo == "Biglietto Giornaliero":
        if not giorni or len(giorni) != 1:
            flash("Seleziona 1 giorno valido per il biglietto", "danger")
            return redirect(url_for("private.reserved"))
        for g in giorni:
            if g not in giorni_validi:
                flash("Seleziona 1 giorno valido per il biglietto", "danger")
                return redirect(url_for("private.reserved"))     

    elif tipo == "Pass 2 Giorni":
        if not giorni or len(giorni) != 2:
            flash("Seleziona 2 giorni validi per il biglietto", "danger")
            return redirect(url_for("private.reserved"))
        for g in giorni:
            if g not in giorni_validi:
                flash("Seleziona 2 giorni validi per il biglietto", "danger")
                return redirect(url_for("private.reserved"))

    stats = biglietti_dao.get_statistiche_biglietti_per_giorno()

    for giorno in giorni:
        if stats.get(giorno) >= 200:
            flash(f"Limite massimo di 200 partecipanti raggiunto per il giorno {giorno}. Riprova con altri giorni.", "danger")
            return redirect(url_for("private.reserved"))

    if not biglietti_dao.add_biglietto(current_user.id, tipo, giorni):
        flash("Errore nell'acquisto del biglietto. Riprova.", "danger")
        return redirect(url_for("private.reserved"))

    flash("Biglietto acquistato con successo!", "success")
    return redirect(url_for("private.reserved"))


# -------------------- organizzatori ------------------

def controlla_sovrapposizione(giorno, palco, nuovo_orario_str, nuova_durata):
    performances_pubblicate = performances_dao.get_performances_pubblicate_by_giorno_palco(giorno, palco)
    nuovo_inizio = datetime.strptime(nuovo_orario_str, "%H:%M")
    nuova_fine = nuovo_inizio + timedelta(minutes=int(nuova_durata))
    for p in performances_pubblicate:
        inizio_esistente = datetime.strptime(p["orario"], "%H:%M")
        fine_esistente = inizio_esistente + timedelta(minutes=int(p["durata"]))
        if (nuovo_inizio < fine_esistente) and (nuova_fine > inizio_esistente):
            return True
    return False

@private_bp.route("/add_bozza", methods=["POST"])
@login_required
def aggiungi_bozza():
    nome_artista = request.form.get("artista")
    giorno = request.form.get("giorno")
    orario = f"{request.form['ora']}:{request.form['minuti']}"  # HH:MM
    durata = request.form.get("durata")
    descrizione = request.form.get("descrizione")
    palco = request.form.get("palco")
    genere = request.form.get("genere")
    file = request.files.get("immagine")

    if controlla_sovrapposizione(giorno, palco, orario, durata):
        flash("Errore: Sovrapposizione orari con una performance già pubblicata", "danger")
        return redirect(url_for("private.reserved"))

    if file and file.filename != "":
        # ultimi 4 caratteri
        estensione = file.filename[-4:]
        nome_file = str(uuid.uuid4()) + estensione
        percorso_cartella = os.path.join(current_app.root_path, "static", "images", "uploaded")
        if not os.path.exists(percorso_cartella):
            os.makedirs(percorso_cartella)
        percorso_completo = os.path.join(percorso_cartella, nome_file)
        file.save(percorso_completo)
        path_db = "/static/images/uploaded/" + nome_file
    else:
        flash("Errore nell'aggiunta della bozza", "danger")
        return redirect(url_for("private.reserved"))

    success = performances_dao.add_bozza(
        nome_artista, giorno, orario, durata, descrizione, palco, genere, path_db, current_user.id
    )

    if not success:
        flash("Errore nell'aggiunta della bozza", "danger")
        return redirect(url_for("private.reserved"))

    flash("Bozza aggiunta con successo!", "success")
    return redirect(url_for("private.reserved"))


@private_bp.route("/publish_bozza/<int:id>", methods=["POST"])
@login_required
def pubblica_bozza(id):
    if current_user.ruolo == "partecipante":
        return redirect(url_for("private.reserved"))
    if not performances_dao.publish_bozza(id, current_user.id):
        flash("Errore nella pubblicazione della bozza")
        return redirect(url_for("private.reserved"))
    flash("Bozza pubblicata con successo!", "success")
    return redirect(url_for("private.reserved"))

@private_bp.route("/modifica_bozza/<int:id>", methods=["GET"])
@login_required
def modifica_bozza(id):
    if current_user.ruolo == "partecipante":
        return redirect(url_for("private.reserved")) 
    bozza = performances_dao.get_bozza_by_id(id)
    if not bozza or bozza["pubblicato"]:
        flash("Bozza non trovata o già pubblicata.", "danger")
        return redirect(url_for("private.reserved"))
    return render_template("private/modifica_bozza.html", bozza=bozza)

from flask import request, flash, redirect, url_for, render_template
from datetime import datetime, timedelta

@private_bp.route("/modifica_bozza/<int:id>", methods=["POST"])
@login_required
def salva_modifiche_bozza(id):
    if current_user.ruolo == "partecipante":
        return redirect(url_for("private.reserved"))

    data = request.form
    orario = f"{data['ora']}:{data['minuti']}"
    durata = data["durata"]

    # Controllo sovrapposizione
    sovrapposta = controlla_sovrapposizione(
        giorno=data["giorno"],
        palco=data["palco"],
        nuovo_orario_str=orario,
        nuova_durata=durata
    )

    if sovrapposta:
        flash("Attenzione: la performance si sovrappone a un'altra già pubblicata!", "danger")
        # Ricarichiamo la bozza per ripopolare il form
        bozza = performances_dao.get_bozza_by_id(id)
        return render_template("private/modifica_bozza.html", bozza=bozza)
    
    success = performances_dao.update_bozza(
        id_performance=id,
        id_organizzatore=current_user.id,
        nome_artista=data["nome_artista"],
        giorno=data["giorno"],
        orario=orario,
        durata=durata,
        descrizione=data["descrizione"],
        palco=data["palco"],
        genere=data["genere"]
    )

    if success:
        flash("Bozza modificata con successo!", "success")
    else:
        flash("Impossibile modificare la bozza", "danger")

    return redirect(url_for("private.reserved"))




