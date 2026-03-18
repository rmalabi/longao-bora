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
        "maps": "https://www.google.com/maps?q=Bora+Sports"
    }
}


def buscar_participantes(ponto_id):
    try:
        response = requests.get(
            TABLE_URL,
            headers=HEADERS,
            params={
                "select": "*",
                "ponto": f"eq.{ponto_id}",
                "order": "created_at.asc"
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("ERRO BUSCAR:", e)
        return []


def inserir_participante(ponto, nome, horario, duracao):
    try:
        requests.post(
            TABLE_URL,
            headers=HEADERS,
            json={
                "ponto": ponto,
                "nome": nome,
                "horario": horario,
                "duracao": duracao
            },
            timeout=10
        )
    except Exception as e:
        print("ERRO INSERIR:", e)


def remover_participante(ponto, participante_id):
    try:
        requests.delete(
            TABLE_URL,
            headers=HEADERS,
            params={
                "id": f"eq.{participante_id}",
                "ponto": f"eq.{ponto}"
            },
            timeout=10
        )
    except Exception as e:
        print("ERRO REMOVER:", e)


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
                <button type="submit" class="remove-btn">Remover</button>
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

            .logo {{
                width: 180px;
                display: block;
                margin: auto;
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
                margin-top: 5px;
                border-radius: 8px;
                border: none;
                background: #10B26C;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }}

            .map-btn {{
                background: black;
            }}

            .remove-btn {{
                background: red;
                width: auto;
                padding: 6px 10px;
            }}

            input {{
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border-radius: 8px;
                border: 1px solid #ccc;
                box-sizing: border-box;
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

            .participants-list {{
                list-style: none;
                padding: 0;
            }}

            .footer {{
                text-align: center;
                margin-top: 30px;
            }}

            .empty {{
                color: #777;
            }}

            @media (max-width: 600px) {{
                .participant-item {{
                    flex-direction: column;
                    align-items: flex-start;
                }}

                .remove-btn {{
                    width: 100%;
                }}
            }}
        </style>
    </head>

    <body>

        <img src="/static/logo.png" class="logo">
        <h1>Cadê você no longão?</h1>
        <h3>Bora Sports</h3>

        <div class="card">
            <h2>{PONTOS['cavaleiros']['nome']}</h2>

            <a href="{PONTOS['cavaleiros']['maps']}" target="_blank">
                <button type="button" class="map-btn">Abrir no GPS</button>
            </a>

            <form action="/entrar/cavaleiros" method="post">
                <input name="nome" placeholder="Seu nome" required>
                <input name="horario" placeholder="Horário" required>
                <input name="duracao" placeholder="Duração" required>
                <button type="submit">Entrar</button>
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
                <input name="horario" placeholder="Horário" required>
                <input name="duracao" placeholder="Duração" required>
                <button type="submit">Entrar</button>
            </form>

            <h4>Participantes</h4>
            {render_participantes("tenda_imbetiba")}
        </div>

        <div class="card">
            <h3>Tecnologias</h3>
            <ul>
                <li>Python</li>
                <li>Flask</li>
                <li>Supabase</li>
                <li>Render</li>
            </ul>
        </div>

        <div class="footer">
            <img src="/static/deeprun.png" style="width:100px;">
        </div>

    </body>
    </html>
    """


@app.route("/entrar/<ponto>", methods=["POST"])
def entrar(ponto):
    inserir_participante(
        ponto,
        request.form["nome"],
        request.form["horario"],
        request.form["duracao"]
    )
    return redirect(url_for("home"))


@app.route("/remover/<ponto>/<int:id>", methods=["POST"])
def remover(ponto, id):
    remover_participante(ponto, id)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)