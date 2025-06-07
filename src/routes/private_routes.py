from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from dao import biglietti_dao, performances_dao

private_bp = Blueprint('private', __name__)

@private_bp.route("/reserved")
@login_required
def reserved():
    stats = biglietti_dao.get_statistiche_biglietti_per_giorno()
    biglietto = biglietti_dao.get_biglietto_by_partecipante(current_user.id)
    if current_user.ruolo == "organizzatore":
        return render_template("private/riservata_organizzatori.html", user=current_user, stats=stats)
    return render_template("private/riservata_partecipanti.html", user=current_user, stats=stats, biglietto=biglietto)

@private_bp.route("/purchase")
def compra_biglietto():
    tipo = request.form.get("tipo")
    giorni = request.form.getlist("giorni")

    tipi_validi = ("Biglietto Giornaliero", "Pass 2 Giorni", "Full Pass")
    giorni_validi = ("Venerdi", "Sabato", "Domenica")

    if not tipo or tipo not in tipi_validi:
        flash("Seleziona un tipo di biglietto valido", "danger")

    if tipo == "Full Pass":
        if set(giorni) != set(giorni_validi):
            flash("Seleziona tutti i giorni per il full pass", "danger")
            return redirect(url_for("private.reserved"))  

    if tipo == "Biglietto Giornaliero":
        if not giorni or len(giorni) != 1:
            flash("Seleziona 1 giorno valido per il biglietto", "danger")
            return redirect(url_for("private.reserved"))
        for g in giorni:
            if g not in giorni_validi:
                flash("Seleziona 1 giorno valido per il biglietto", "danger")
                return redirect(url_for("private.reserved"))     
               
    if tipo == "Pass 2 Giorni":
        if not giorni or len(giorni) != 2:
            flash("Seleziona 2 giorni validi per il biglietto", "danger")
            return redirect(url_for("private.reserved"))
        for g in giorni:
            if g not in giorni_validi:
                flash("Seleziona 2 giorni validi per il biglietto", "danger")
                return redirect(url_for("private.reserved"))     

    if not biglietti_dao.add_biglietto(current_user.id, tipo, giorni):
        flash("Errore nell'acquisto del biglietto. Riprova.", "danger")
        return redirect(url_for("private.reserved"))
    flash("Biglietto acquistato con successo!", "success")
    return redirect(url_for("private.reserved"))

# logica per la generazione dello uuid delle immagini

@private_bp.route("/add_bozza")
def aggiungi_bozza():
    nome_artista = request.form.get("nome_artista")
    giorno = request.form.get("giorno")
    orario = request.form.get("orario")
    durata = request.form.get("durata")
    descrizione = request.form.get("descrizione")
    palco = request.form.get("palco")
    genere = request.form.get("genere")
    if not performances_dao.add_bozza(nome_artista, giorno, orario, durata, descrizione, palco, genere, current_user.id):
        flash("Errore nell'aggiunta della bozza", "danger")
        return redirect(url_for("private.reserved"))
    flash("Bozza aggiunta con successo!", "success")
    return redirect(url_for("private.reserved"))

@private_bp.route("/publish_bozza")
def pubblica_bozza():
    id_performance = request.form.get("id_performance")
    if not performances_dao.publish_bozza(id_performance, current_user.id):
        flash("Errore nella pubblicazione della bozza");
        return redirect(url_for("private.reserved"))
    flash("Bozza pubblicata con successo!", "success")
    return redirect(url_for("private.reserved"))

