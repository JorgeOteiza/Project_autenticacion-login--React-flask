from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from api.models import db, User
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api, resources={r"/*": {"origins": "*"}})

# Ruta para el saludo
@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend."
    }
    return jsonify(response_body), 200

# Ruta para registro de usuarios
@api.route('/', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201

# CRUD de usuarios

# Obtener todos los usuarios
@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# Obtener un usuario por su ID
@api.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar un usuario
@api.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email:
        user.email = email
    if password:
        user.set_password(password)

    db.session.commit()
    return jsonify(user.serialize()), 200

# Eliminar un usuario
@api.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
