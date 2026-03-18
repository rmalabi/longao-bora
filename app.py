from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Longão Bora</h1>
    <p>App online.</p>
    <p>Se você está vendo isso, o Render está funcionando.</p>
    """

@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)