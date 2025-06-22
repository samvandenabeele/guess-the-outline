from flask import Blueprint, render_template, request, redirect, url_for, session, send_file
from flask_login import login_required, current_user
import os, random
from .models import Score
from . import db

main = Blueprint('main', __name__)

SVG_FOLDER = "app/static/svgs"
COUNTRIES = [f.split('_')[0] for f in os.listdir(SVG_FOLDER) if '_1.svg' in f]

@main.route("/")
def home():
    return redirect(url_for("main.practice"))

@main.route("/practice", methods=["GET", "POST"])
@login_required
def practice():
    if "current_country" not in session:
        session["current_country"] = random.choice(COUNTRIES)
        session["level"] = 1
        session["rotation"] = random.choice([0, 90, 180, 270])
        session["flip"] = random.choice([False, True])
        session["attempts"] = 0

    country = session["current_country"]
    level = session["level"]
    svg_path = f"svgs/{country}_{level}.svg"

    transform = ""
    if session["flip"]:
        transform += "scaleX(-1) "
    transform += f"rotate({session['rotation']}deg)"

    if request.method == "POST":
        guess = request.form["guess"].strip().lower()
        session["attempts"] += 1
        if guess == country.lower():
            db.session.add(Score(user_id=current_user.id, country=country, attempts=session["attempts"]))
            db.session.commit()
            flash = "Correct!"
            session.clear()
            return redirect(url_for("main.practice"))
        else:
            session["level"] = min(3, session["level"] + 1)

    return render_template("practice.html", svg_path=svg_path, transform=transform)

@main.route("/leaderboard")
def leaderboard():
    scores = Score.query.all()
    leaderboard = {}
    for score in scores:
        leaderboard[score.user.username] = leaderboard.get(score.user.username, 0) + (4 - score.attempts)
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    return render_template("leaderboard.html", leaderboard=sorted_leaderboard)

@main.route("/static/styles.css")
def styles():
    return send_file("styles/styles.css")
