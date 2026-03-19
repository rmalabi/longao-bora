import os
import requests
from flask import Flask, request, redirect, url_for

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
        r = requests.get(
            TABLE_URL,
            headers=HEADERS,
            params={"select": "*", "order": "created_at.asc"},
            timeout=5
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("ERRO BUSCAR:", e)
        return []


def inserir(nome, horario, duracao, ponto):
    try:
        r = requests.post(
            TABLE_URL,
            headers=HEADERS,
            json={
                "nome": nome,
                "horario": horario,
                "duracao": duracao,
                "ponto": ponto
            },
            timeout=5
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print("ERRO INSERIR:", e)
        return False


@app.route("/healthz")
def healthz():
    return "ok", 200


@app.route("/")
def home():
    lista = buscar()

    itens = ""
    for p in lista:
        itens += f"<li>{p.get('nome')} - {p.get('horario')} - {p.get('duracao')} - {p.get('ponto')}</li>"

    return f"""
    <h1>Longão Bora</h1>

    <form action="/add" method="post">
        <input name="nome" placeholder="Nome" required><br><br>
        <input name="horario" placeholder="Horário" required><br><br>
        <input name="duracao" placeholder="Duração" required><br><br>
        <input name="ponto" placeholder="Ponto" required><br><br>
        <button type="submit">Adicionar</button>
    </form>

    <p>Participantes:</p>
    <ul>{itens}</ul>
    """


@app.route("/add", methods=["POST"])
def add():
    inserir(
        request.form["nome"],
        request.form["horario"],
        request.form["duracao"],
        request.form["ponto"]
    )
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)