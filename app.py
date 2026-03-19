import os
import requests
from flask import Flask

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

TABLE_URL = f"{SUPABASE_URL}/rest/v1/participantes_longao"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}


def buscar():
    try:
        r = requests.get(TABLE_URL, headers=HEADERS, params={"select": "*"}, timeout=5)
        return r.json()
    except:
        return []


@app.route("/healthz")
def healthz():
    return "ok", 200


@app.route("/")
def home():
    lista = buscar()

    itens = ""
    for p in lista:
        itens += f"<li>{p.get('nome')} - {p.get('horario')}</li>"

    return f"""
    <h1>Longão Bora</h1>
    <p>Participantes:</p>
    <ul>{itens}</ul>
    """


if __name__ == "__main__":
    app.run(debug=True)