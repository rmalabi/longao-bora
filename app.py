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

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/")
def home():
    try:
        response = requests.get(
            TABLE_URL,
            headers=HEADERS,
            params={"select": "*"},
            timeout=5
        )

        print("STATUS:", response.status_code)

        if response.status_code == 200:
            return f"<h1>OK Supabase</h1><pre>{response.json()}</pre>"
        else:
            return f"<h1>Erro Supabase</h1><p>Status: {response.status_code}</p><p>{response.text}</p>"

    except Exception as e:
        return f"<h1>Erro conexão</h1><p>{e}</p>"

if __name__ == "__main__":
    app.run(debug=True)