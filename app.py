from flask import Flask, jsonify
from flask_cors import CORS
from database import get_all_acces, init_database

app = Flask(__name__)
CORS(app)

init_database()

@app.route("/")
def home():
    return "Backend gestion accès véhicules - OK"

@app.route("/api/acces", methods=["GET"])
def api_acces():
    acces = get_all_acces()
    result = []
    for a in acces:
        result.append({
            "matricule": a["matricule"],
            "date_heure": a["date_heure"],
            "statut": a["statut"]
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)