from flask import Blueprint, render_template, request, redirect, url_for, flash
from dao import performances_dao

public_bp = Blueprint('public', __name__)

@public_bp.route("/")
def home():
    ultime_performances = performances_dao.get_ultime_performances_pubblicate()
    return render_template("public/home.html", performances=ultime_performances)

@public_bp.route("/performances")
def performances():
    n = performances_dao.get_numero_performance_pubblicate()
    giorno = request.args.get('giorno')
    palco = request.args.get('palco')
    genere = request.args.get('genere')

    filtri_presenti = False

    if giorno in ('Venerdi', 'Sabato', 'Domenica'):
        filtri_presenti = True
    if palco in ('Palco A', 'Palco B', 'Palco C'):
        filtri_presenti = True
    if genere in ('Rock', 'Pop', 'Jazz', 'Electronic', 'Hip-Hop', 'Classica'):
        filtri_presenti = True

    if filtri_presenti:
        performances = performances_dao.get_performances_filtrate(giorno, palco, genere)
    else:
        performances = performances_dao.get_performances_ordinate()

    return render_template("public/performances.html", performances=performances, numero_performance=n)

@public_bp.route("/performances/<int:id>")
def performance(id):
    perf = performances_dao.get_performance_by_id(id)
    return render_template("public/performance.html", performance=perf)