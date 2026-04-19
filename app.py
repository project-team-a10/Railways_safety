from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
import random
import time
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = "railguard_secret_key"

app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID")
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET")

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# 👥 Dummy Users
USERS = {
    "admin": {"password": "admin123", "role": "authority"},
    "guest": {"password": "guest123", "role": "guest"}
}

# ── Train models ──
from models.trainer import registry
registry.train_all()

from data.indian_railways_data import (
    IR_ZONES, MAJOR_STATIONS, ACCIDENT_TYPES, SEASONS,
    ACCIDENT_YEAR_DATA, FEATURE_NAMES, LABELS
)

# ── LOGIN ──
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = USERS.get(username)

        if user and user["password"] == password:
            session["user"] = username
            session["role"] = user["role"]
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# 🔐 GOOGLE LOGIN START
@app.route("/google-login")
def google_login():
    return google.authorize_redirect(url_for("auth", _external=True))


@app.route("/auth")
def auth():
    token = google.authorize_access_token()
    
    # Get user info safely
    user_info = token.get("userinfo")
    if not user_info:
        user_info = google.get("userinfo").json()

    session["user"] = user_info["email"]
    session["role"] = "authority"

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ── HOME ──
@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        role=session.get("role"),
        user=session.get("user"),
        zones=IR_ZONES,
        stations=MAJOR_STATIONS,
        accident_types=ACCIDENT_TYPES,
        seasons=SEASONS,
        year_data=ACCIDENT_YEAR_DATA,
        feature_names=FEATURE_NAMES,
        labels=LABELS,
        model_infos=registry.get_model_infos(),
    )


# ── APIs ──
@app.route("/api/live_sensor_stream")
def live_sensor_stream():
    data = {
        "timestamp": time.strftime("%H:%M:%S"),
        "tp2_pressure": round(random.uniform(8.1, 8.4), 2),
        "oil_temperature": round(random.uniform(62.0, 78.0), 2),
        "motor_current": round(random.uniform(51.0, 54.5), 1),
        "status": "Healthy"
    }

    if random.random() > 0.95:
        data["oil_temperature"] = round(random.uniform(95.0, 115.0), 2)
        data["status"] = "Critical Alert - Overheating"

    return jsonify(data)


@app.route("/api/predict", methods=["POST"])
def predict():
    if session.get("role") != "authority":
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    results = registry.predict_all(data)
    return jsonify({"status": "ok", "results": results})


@app.route("/api/zones")
def get_zones():
    return jsonify(IR_ZONES)


@app.route("/api/stations")
def get_stations():
    return jsonify(MAJOR_STATIONS)


@app.route("/api/year_data")
def get_year_data():
    return jsonify(ACCIDENT_YEAR_DATA)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)