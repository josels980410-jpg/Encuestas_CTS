from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "cts_secret_key_123"  # Cambia esta clave por una más segura en producción

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
        "https://app.powerbi.com/view?r=PRIMER_ENLACE",  # Reemplaza con tu enlace real
        "https://app.powerbi.com/view?r=SEGUNDO_ENLACE"  # Reemplaza con tu enlace real
    ]
    return render_template("dashboard.html", powerbi_urls=powerbi_urls, user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# ------------------- EJECUCIÓN -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
