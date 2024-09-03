from flask import Blueprint, request, jsonify

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Lógica de autenticación
    if email == "usuario@example.com" and password == "contraseña":
        return jsonify({"token": "fake-jwt-token", "user": {"id": 1, "email": email}}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
