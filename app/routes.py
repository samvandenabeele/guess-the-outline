from flask import Blueprint, render_template, request, redirect, url_for, session, send_file, flash
from flask_login import login_required, current_user
import os, random
from .models import Score, Country
from . import db
import string

main = Blueprint('main', __name__)

SVG_FOLDER = "app/static/svgs"
COUNTRIES = [f.split('_')[0] for f in os.listdir(SVG_FOLDER) if '_1.svg' in f]

@main.route("/")
def home():
    return redirect(url_for("main.practice"))

@main.route("/practice", methods=["GET", "POST"])
@login_required
def practice():
    if "country_key" not in session:
        country = random.choice(COUNTRIES)
        country_key = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        db.session.add(Country(name=country, key=country_key))
        db.session.commit()

        session["country_key"] = country_key
        session["level"] = 1
        session["rotation"] = random.choice([0, 90, 180, 270])
        session["flip"] = random.choice([False, True])
        session["attempts"] = 0
    else:
        print("Session already has country_key:", session["country_key"])

    options = COUNTRIES
    print("Available countries:", options)

    country_key = session["country_key"]
    level = session["level"]
    country_obj = Country.query.filter_by(key=country_key).first()
    country = country_obj.name
    svg_path = f"{country_key}_{level}.svg"

    transform = ""
    if session["flip"]:
        transform += "scaleX(-1) "
    transform += f"rotate({session['rotation']}deg)"

    if request.method == "POST":
        guess = request.form["guess"].strip().lower()
        session["attempts"] += 1
        if guess == country.lower():
            for key in ["current_country", "rotation", "flip", "attempts", "country_key"]:
                session.pop(key, None)
            return redirect(url_for("main.correct"))
        else:
            session["level"] = session['level'] + 1
            if session["level"] > 3:
                for key in ["current_country", "level", "rotation", "flip", "attempts", "country_key"]:
                    session.pop(key, None)
                return redirect(url_for("main.lost"))

    return render_template("practice.html", svg_path=svg_path, transform=transform, options=options)

@main.route("/daily-puzzle", methods=["GET", "POST"])
@login_required
def daily():
    if "country_key" not in session:
        country = random.choice(COUNTRIES)
        country_key = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        db.session.add(Country(name=country, key=country_key))
        db.session.commit()

        session["country_key"] = country_key
        session["level"] = 1
        session["rotation"] = random.choice([0, 90, 180, 270])
        session["flip"] = random.choice([False, True])
        session["attempts"] = 0
    else:
        print("Session already has country_key:", session["country_key"])

    options = COUNTRIES
    print("Available countries:", options)

    country_key = session["country_key"]
    level = session["level"]
    country_obj = Country.query.filter_by(key=country_key).first()
    country = country_obj.name
    svg_path = f"{country_key}_{level}.svg"

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
            for key in ["current_country", "rotation", "flip", "attempts", "country_key"]:
                session.pop(key, None)
            return redirect(url_for("main.correct"))
        else:
            session["level"] = session['level'] + 1
            if session["level"] > 3:
                for key in ["current_country", "level", "rotation", "flip", "attempts", "country_key"]:
                    session.pop(key, None)
                return redirect(url_for("main.lost"))

    return render_template("practice.html", svg_path=svg_path, transform=transform, options=options)

@main.route("/leaderboard")
def leaderboard():
    scores = Score.query.all()
    leaderboard = {}
    for score in scores:
        leaderboard[score.user.username] = leaderboard.get(score.user.username, 0) + (4 - score.attempts)
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    return render_template("leaderboard.html", leaderboard=sorted_leaderboard)

@main.route("/daily-solved")
@login_required
def daily_solved():
    return render_template("daily_solved.html")

@main.route("/static/styles.css")
def styles():
    return send_file("styles/styles.css")

@main.route('/images/<path:key>_<level>.svg')
def svg(key, level):
    country_obj = Country.query.filter_by(key=key).first()
    if not country_obj:
        print(f"Country with key {key} not found.")
        return "SVG not found", 404
    country_name = country_obj.name
    svg_path = f"static/svgs/{country_name}_{level}.svg"
    print(f"Serving SVG from path: {svg_path}")
    return send_file(svg_path, download_name=f"{key}_{level}.svg", )

@main.route("/lost")
@login_required
def lost():
    return render_template("lost.html")

@main.route("/correct")
@login_required
def correct():
    return render_template("correct.html")

@main.route("/close-session", methods=["POST"])
@login_required
def close_session():
    for key in ["current_country", "level", "rotation", "flip", "attempts", "country_key"]:
        session.pop(key, None)
    return '', 204  # No content