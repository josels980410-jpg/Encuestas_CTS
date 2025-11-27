import os
import time
import json
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta

# ------------------- ZONA HORARIA -------------------
os.environ['TZ'] = 'America/Mexico_City'
time.tzset()

# ------------------- CONFIGURACIÓN FLASK -------------------
app = Flask(__name__)
app.secret_key = "cts_secret_key_123"
app.permanent_session_lifetime = timedelta(minutes=30)


# ------------------- GOOGLE SHEETS -------------------
GOOGLE_SHEETS_ID = "1rNtbNAbpcn8HpM4rl8OJ538kqQJKQDzYEzIFsI2TluQ"
CREDENCIALES_JSON = "credenciales_google/credenciales_google.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

sheet = None
try:
    if os.path.exists(CREDENCIALES_JSON):
        credentials = Credentials.from_service_account_file(
            CREDENCIALES_JSON, scopes=SCOPES
        )
        print("🔑 Credenciales cargadas desde archivo local.")
    else:
        google_credentials_env = os.environ.get("GOOGLE_CREDENTIALS")
        if google_credentials_env:
            creds_info = json.loads(google_credentials_env)
            credentials = Credentials.from_service_account_info(
                creds_info, scopes=SCOPES
            )
            print("🔑 Credenciales cargadas desde variable de entorno.")
        else:
            raise Exception("No se encontraron credenciales")

    client = gspread.authorize(credentials)
    sheet = client.open_by_key(GOOGLE_SHEETS_ID).sheet1
    print("✅ Conexión exitosa con Google Sheets.")

except Exception as e:
    print("❌ Error conectando con Google Sheets:", e)
    sheet = None

# ------------------- USUARIOS -------------------
# Puedes definir aquí los usuarios válidos
USUARIOS = {
    "Lalo_Luna": "y3#+P(4v[N6(",
    "Jose_Consultor": "654321987"
}

# ------------------- RUTAS -------------------

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html", error=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USUARIOS and USUARIOS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Usuario o contraseña incorrectos"
            return render_template("login.html", error=error)
    return render_template("login.html", error=None)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))
    # Aquí insertaremos tus iframes de Power BI en el template
    powerbi_urls = [
        "https://app.powerbi.com/view?r=eyJrIjoiY2IwNzU0YTItZTNiMi00NDVmLWJmYTktYWM5MTQ0ZTJlNWUxIiwidCI6IjAzODk5MTIxLWQ5NzYtNDRlOS1iODI0LTFmYzU1N2JmZGRjZSJ9",
        "https://app.powerbi.com/view?r=eyJrIjoiYWY4NDA4OTgtYzhiNy00NzE3LWFmZDQtMDRiNmM2YzIzYzg4IiwidCI6IjAzODk5MTIxLWQ5NzYtNDRlOS1iODI0LTFmYzU1N2JmZGRjZSJ9" 
    ]
    return render_template("dashboard.html", powerbi_urls=powerbi_urls, user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# ------------------- EJECUCIÓN -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
