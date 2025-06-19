from flask import Flask, render_template, request, jsonify, session
import random
import json
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"  # for session

with open("static/countries.json") as f:
    countries = json.load(f)

@app.route("/")
def index():
    # Choose a random country
    country = random.choice(countries)
    session["country"] = country["name"]
    session["step"] = 1
    return render_template("index.html", image=country["images"][0])

@app.route("/guess", methods=["POST"])
def guess():
    user_guess = request.form["guess"].strip().lower()
    actual = session.get("country", "").lower()
    step = session.get("step", 1)

    if user_guess == actual:
        return jsonify({"result": "correct"})
    else:
        step += 1
        session["step"] = step
        for c in countries:
            if c["name"].lower() == actual:
                if step <= len(c["images"]):
                    return jsonify({
                        "result": "wrong",
                        "next_image": c["images"][step - 1]
                    })
                else:
                    return jsonify({"result": "failed", "answer": actual})
        return jsonify({"result": "error"})

if __name__ == "__main__":
    app.run(debug=True)
