from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from my_ml_model import predict_preference
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, "adaptive_ui.db")


def get_db_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("Database location:")
    print(DATABASE)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/api/interaction", methods=["POST"])
def record_interaction():

    data = request.get_json()

    action = data.get("action")

    if not action:

        return jsonify({
            "success": False,
            "message": "No action received"
        }), 400


    connection = get_db_connection()

    connection.execute(
        "INSERT INTO interactions (action) VALUES (?)",
        (action,)
    )

    connection.commit()
    connection.close()


    print("Saved interaction:", action)


    return jsonify({
        "success": True,
        "action": action
    })



@app.route("/api/interactions")
def get_interactions():

    connection = get_db_connection()

    rows = connection.execute("""
        SELECT id, action, timestamp
        FROM interactions
        ORDER BY id ASC
    """).fetchall()

    connection.close()


    interactions = []

    for row in rows:

        interactions.append({
            "id": row["id"],
            "action": row["action"],
            "timestamp": row["timestamp"]
        })


    return jsonify({
        "interactions": interactions
    })



@app.route("/api/preferences")
def get_preferences():

    connection = get_db_connection()

    rows = connection.execute("""
        SELECT action, COUNT(*) AS count
        FROM interactions
        WHERE action IN (
            'Dashboard',
            'Analytics',
            'Settings'
        )
        GROUP BY action
    """).fetchall()

    connection.close()


    counts = {
        "Dashboard": 0,
        "Analytics": 0,
        "Settings": 0
    }


    for row in rows:

        counts[row["action"]] = row["count"]


    highest = max(counts.values())


    if highest == 0:

        preferred_feature = "None"

    else:

        preferred_feature = max(
            counts,
            key=counts.get
        )


    return jsonify({
        "counts": counts,
        "preferred_feature": preferred_feature
    })
@app.route("/api/ml-preference")
def get_ml_preference():

    result = predict_preference()

    return jsonify(result)



if __name__ == "__main__":

    initialize_database()

    app.run(debug=True)