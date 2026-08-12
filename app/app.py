from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")


def check_database():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=2
        )
        conn.close()
        return True
    except Exception:
        return False


@app.route("/")
def home():
    return jsonify({
        "application": "kind-devops-cicd",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/ready")
def ready():
    if check_database():
        return jsonify({"status": "ready"}), 200

    return jsonify({"status": "not ready"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
