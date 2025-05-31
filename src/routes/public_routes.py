from flask import Blueprint, render_template, request, redirect, url_for, flash
from dao import performances_dao

public_bp = Blueprint('public', __name__)

@public_bp.route("/")
def home():
    ultime_performances = performances_dao.get_ultime_performances_pubblicate()
    return render_template("public/home.html", performances=ultime_performances)
