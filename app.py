from flask import Flask, request, redirect, url_for

app = Flask(__name__)

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

participantes = {
    "cavaleiros": [],
    "tenda_imbetiba": []
}

proximo_id = 1


def render_participantes(ponto_id):
    lista = participantes[ponto_id]

    if not lista:
        return '<p class="empty">Ainda ninguém marcou esse ponto.</p>'

    itens = ""
    for item in lista:
        participante_id = item["id"]
        nome = item["nome"]
        horario = item["horario"]
        duracao = item["duracao"]

        itens += f"""
        <li class="participant-item">
            <span><strong>{nome}</strong> — saída: {horario} — treino: {duracao}</span>
            <form action="/remover/{ponto_id}/{participante_id}" method="post" class="remove-form">
                <button type="submit" class="remove-btn">Remover</button>
            </form>
        </li>
        """

    return f'<ul class="participants-list">{itens}</ul>'


@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
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
                width: 220px;
                display: block;
                margin: 0 auto 10px auto;
            }}

            h1 {{
                text-align: center;
                margin-bottom: 4px;
            }}

            h3 {{
                text-align: center;
                color: #555;
                margin-top: 0;
            }}

            .subtitle {{
                text-align: center;
                margin-bottom: 20px;
            }}

            .card {{
                background: white;
                padding: 20px;
                margin-top: 18px;
                border-radius: 14px;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            }}

            .actions {{
                margin-bottom: 12px;
            }}

            button {{
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
                background: #10B26C;
                color: white;
                font-weight: bold;
                cursor: pointer;
                margin-top: 5px;
            }}

            button:hover {{
                background: #0C8A54;
            }}

            .map-btn {{
                background: #1E1E1E;
            }}

            .map-btn:hover {{
                background: #000;
            }}

            .remove-btn {{
                background: #B3261E;
                padding: 8px 12px;
                font-size: 12px;
                margin-top: 0;
            }}

            .remove-btn:hover {{
                background: #8C1C16;
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
                padding-left: 0;
                margin-top: 10px;
            }}

            .participant-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }}

            .participant-item:last-child {{
                border-bottom: none;
            }}

            .remove-form {{
                margin: 0;
            }}

            .empty {{
                color: #777;
            }}

            @media (max-width: 600px) {{
                .participant-item {{
                    flex-direction: column;
                    align-items: flex-start;
                }}

                .remove-form {{
                    width: 100%;
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

        <p class="subtitle">
            Escolha seu ponto de saída e informe horário + duração.
        </p>

        <div class="card">
            <h2>📍 {PONTOS['cavaleiros']['nome']}</h2>

            <div class="actions">
                <a href="{PONTOS['cavaleiros']['maps']}" target="_blank">
                    <button type="button" class="map-btn">Abrir no GPS</button>
                </a>
            </div>

            <form action="/entrar/cavaleiros" method="post">
                <input type="text" name="nome" placeholder="Seu nome" required>
                <input type="text" name="horario" placeholder="Horário de partida (ex: 05:20)" required>
                <input type="text" name="duracao" placeholder="Duração (ex: 2h, 1h45)" required>

                <button type="submit">Entrar nesse ponto</button>
            </form>

            <h4>Participantes</h4>
            {render_participantes("cavaleiros")}
        </div>

        <div class="card">
            <h2>📍 {PONTOS['tenda_imbetiba']['nome']}</h2>

            <div class="actions">
                <a href="{PONTOS['tenda_imbetiba']['maps']}" target="_blank">
                    <button type="button" class="map-btn">Abrir no GPS</button>
                </a>
            </div>

            <form action="/entrar/tenda_imbetiba" method="post">
                <input type="text" name="nome" placeholder="Seu nome" required>
                <input type="text" name="horario" placeholder="Horário de partida (ex: 05:30)" required>
                <input type="text" name="duracao" placeholder="Duração (ex: 2h)" required>

                <button type="submit">Entrar nesse ponto</button>
            </form>

            <h4>Participantes</h4>
            {render_participantes("tenda_imbetiba")}
        </div>

    </body>
    </html>
    """


@app.route("/entrar/<ponto>", methods=["POST"])
def entrar(ponto):
    global proximo_id

    nome = request.form.get("nome", "").strip()
    horario = request.form.get("horario", "").strip()
    duracao = request.form.get("duracao", "").strip()

    if ponto in participantes and nome and horario and duracao:
        participantes[ponto].append({
            "id": proximo_id,
            "nome": nome,
            "horario": horario,
            "duracao": duracao
        })
        proximo_id += 1

    return redirect(url_for("home"))


@app.route("/remover/<ponto>/<int:participante_id>", methods=["POST"])
def remover(ponto, participante_id):
    if ponto in participantes:
        participantes[ponto] = [
            item for item in participantes[ponto]
            if item["id"] != participante_id
        ]

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)