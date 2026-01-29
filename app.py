from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Mes codes admin secrets
ADMIN_PSEUDO = "Los_Mobilis"
ADMIN_CODE = "Ttsacause_simon!"

def log_login(pseudo):
    if not pseudo:
        return
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logins.txt", "a", encoding="utf-8") as f:
        f.write(f"{now} | pseudo={pseudo}\n")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pseudo = request.form.get('pseudo')
        code = request.form.get('code')

        # Sécurité anti vide
        if not pseudo:
            return "Pseudo manquant", 400

        # Log pseudo + heure
        log_login(pseudo)

        # Vérifier si c'est moi (admin)
        if pseudo == ADMIN_PSEUDO and code == ADMIN_CODE:
            return redirect(url_for('secret'))  # page secrète

        # Tous les autres
        return redirect(url_for('success', pseudo=pseudo))

    return render_template('login.html')


@app.route('/secret')
def secret():
    logs = []

    try:
        with open("logins.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if " | pseudo=" in line:
                    date_part, pseudo_part = line.split(" | pseudo=")
                    logs.append({
                        "date": date_part,
                        "pseudo": pseudo_part
                    })
    except FileNotFoundError:
        logs = []

    # Trier du plus récent au plus ancien
    logs = list(reversed(logs))

    return render_template('secret.html', logs=logs)


@app.route('/success', methods=['GET', 'POST'])
def success():
    pseudo = request.values.get('pseudo')
    print("ARRIVÉ SUR /success avec méthode =", request.method)
    return render_template('success.html', pseudo=pseudo)


if __name__ == '__main__':
    app.run(debug=True)
