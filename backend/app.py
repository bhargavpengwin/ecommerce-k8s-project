from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api")
def home():
    return jsonify({
        "message": "Welcome to E-Commerce Backend"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)