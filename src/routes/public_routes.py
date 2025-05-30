from flask import Blueprint, render_template, request, redirect, url_for, flash

public_bp = Blueprint('public', __name__)

@public_bp.route("/")
def home():
    return render_template("public/home.html")