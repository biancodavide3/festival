from flask import Blueprint, render_template, request, redirect, url_for, flash
from dao import performances_dao

public_bp = Blueprint('public', __name__)

@public_bp.route("/")
def home():
    ultime_performances = performances_dao.get_ultime_performances_pubblicate()
    return render_template("public/home.html", performances=ultime_performances)

@public_bp.route("/performances")
def performances():
    performances_ordinate = performances_dao.get_performances_ordinate()
    return render_template("public/performances.html", performances=performances_ordinate)

@public_bp.route("/performances/<int:id>")
def performance(id):
    perf = performances_dao.get_performance_by_id(id)
    return render_template("public/performance.html", performance=perf)