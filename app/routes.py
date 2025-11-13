from flask import Blueprint, jsonify

# Membuat blueprint utama
main = Blueprint("main", __name__)

# Route utama (root)
@main.route("/")
def home():
    return jsonify({
        "message": "Matrix Regression Flask API is running successfully 🚀"
    })
