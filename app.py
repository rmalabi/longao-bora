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

PONTOS = {
    "cavaleiros": {
        "nome": "Posto 1 - Cavaleiros",
        "maps": "https://www.google.com/maps?q=Posto+1+Cavaleiros+Macae"
    },
    "tenda_imbetiba": {
        "nome": "Tenda Imbetiba",
        "maps": "https://www.google.com/maps?q=Imbetiba+Macae"
    }
}


def buscar_participantes(ponto_id):
    try:
        r = requests.get(
            TABLE_URL,
            headers=HEADERS,
            params={
                "select": "*",
                "ponto": f"eq.{ponto_id}",
                "order": "created_at.asc"
            },
            timeout=5
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("ERRO BUSCAR:", e)
        return []


def inserir_participante(ponto, nome, horario, duracao):
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


def remover_participante(item_id):
    try:
        r = requests.delete(
            TABLE_URL,
            headers=HEADERS,
            params={"id": f"eq.{item_id}"},
            timeout=5
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print("ERRO REMOVER:", e)
        return False


def render_participantes(ponto_id):
    lista = buscar_participantes(ponto_id)

    if not lista:
        return '<p class="empty">Ainda ninguém marcou esse ponto.</p>'

    itens = ""
    for item in lista:
        itens += f"""
        <li class="participant-item">
            <span><strong>{item["nome"]}</strong> — saída: {item["horario"]} — treino: {item["duracao"]}</span>

            <form action="/remover/{ponto_id}/{item["id"]}" method="post">
                <button type="submit" class="remove-btn">❌</button>
            </form>
        </li>
        """

    return f'<ul class="participants-list">{itens}</ul>'


@app.route("/healthz")
def healthz():
    return "ok", 200


@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Longão Bora</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #F4F6F8;
                padding: 20px;
                max-width: 700px;
                margin: auto;
                color: #1E1E1E;
            }}

            .logo-top {{
                text-align: center;
                margin-bottom: 10px;
            }}

            h1 {{
                text-align: center;
                margin-bottom: 5px;
            }}

            h3 {{
                text-align: center;
                color: #666;
                margin-top: 0;
            }}

            .subtitle {{
                text-align: center;
                margin-bottom: 20px;
            }}

            .card {{
                background: white;
                padding: 20px;
                margin-top: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}

            button {{
                width: 100%;
                padding: 10px;
                margin-top: 8px;
                border-radius: 8px;
                border: none;
                background: #10B26C;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }}

            .map-btn {{
                background: #111;
            }}

            .remove-btn {{
                background: red;
                width: auto;
                padding: 6px 10px;
                margin-left: 10px;
                margin-top: 0;
            }}

            input {{
                width: 100%;
                padding: 10px;
                margin-top: 8px;
                border-radius: 8px;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }}

            .participants-list {{
                list-style: none;
                padding: 0;
                margin-top: 10px;
            }}

            .participant-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
                margin-top: 10px;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }}

            .participant-item:last-child {{
                border-bottom: none;
            }}

            .empty {{
                color: #777;
            }}

            .footer {{
                text-align: center;
                margin-top: 30px;
            }}

            @media (max-width: 600px) {{
                .participant-item {{
                    flex-direction: column;
                    align-items: flex-start;
                }}

                .remove-btn {{
                    width: 100%;
                    margin-left: 0;
                }}
            }}
        </style>
    </head>

    <body>
        <div class="logo-top">
            <img src="/static/logo.png" style="width:160px;">
            <br>
            <img src="/static/deeprun.png" style="width:100px; margin-top:10px;">
        </div>

        <h1>Cadê você no longão?</h1>
        <h3>Bora Sports</h3>
        <p class="subtitle">Escolha seu ponto de saída e informe horário + duração.</p>

        <div class="card">
            <h2>{PONTOS['cavaleiros']['nome']}</h2>

            <a href="{PONTOS['cavaleiros']['maps']}" target="_blank">
                <button type="button" class="map-btn">Abrir no GPS</button>
            </a>

            <form action="/entrar/cavaleiros" method="post">
                <input name="nome" placeholder="Seu nome" required>
                <input name="horario" placeholder="Horário (ex: 05:20)" required>
                <input name="duracao" placeholder="Duração (ex: 2h)" required>
                <button type="submit">Entrar nesse ponto</button>
            </form>

            <h4>Participantes</h4>
            {render_participantes("cavaleiros")}
        </div>

        <div class="card">
            <h2>{PONTOS['tenda_imbetiba']['nome']}</h2>

            <a href="{PONTOS['tenda_imbetiba']['maps']}" target="_blank">
                <button type="button" class="map-btn">Abrir no GPS</button>
            </a>

            <form action="/entrar/tenda_imbetiba" method="post">
                <input name="nome" placeholder="Seu nome" required>
                <input name="horario" placeholder="Horário (ex: 05:30)" required>
                <input name="duracao" placeholder="Duração (ex: 2h)" required>
                <button type="submit">Entrar nesse ponto</button>
            </form>

            <h4>Participantes</h4>
            {render_participantes("tenda_imbetiba")}
        </div>

        <div class="card">
            <h3>🚀 Tecnologias</h3>
            <ul>
                <li>Python</li>
                <li>Flask</li>
                <li>Supabase</li>
                <li>Render</li>
            </ul>
        </div>

        <div class="footer">
            <img src="/static/deeprun.png" style="width:100px;">
            <p>Powered by Deep Run 🐢🍺</p>
        </div>
    </body>
    </html>
    """


@app.route("/entrar/<ponto>", methods=["POST"])
def entrar(ponto):
    if ponto in PONTOS:
        inserir_participante(
            ponto,
            request.form["nome"],
            request.form["horario"],
            request.form["duracao"]
        )
    return redirect(url_for("home"))


@app.route("/remover/<ponto>/<int:id>", methods=["POST"])
def remover(ponto, id):
    if ponto in PONTOS:
        remover_participante(id)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)