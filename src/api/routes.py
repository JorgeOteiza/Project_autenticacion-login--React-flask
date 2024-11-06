from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import db, User

api = Blueprint('api', __name__)

@api.route('/hello', methods=['GET'])
def handle_hello():
    return jsonify({"message": "Hello! I'm a message from the backend."}), 200

@api.route('/signup', methods=['OPTIONS', 'POST'])
def signup():
    # Respuesta rápida para solicitudes OPTIONS de preflight CORS
    if request.method == 'OPTIONS':
        return '', 204

    # Manejar registro en solicitudes POST
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validar datos
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Verificar si el usuario ya existe
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User already exists"}), 400

    # Crear nuevo usuario
    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    token = create_access_token(identity=new_user.id)

    return jsonify({
        "message": "User created successfully!",
        "user": {
            "id": new_user.id,
            "email": new_user.email
        },
        "token": token
    }), 201

@api.route('/private/<int:id>', methods=['GET'])
@jwt_required(optional=True)
def protected_route():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "message": "This is a protected route",
        "user": {
            "id": user.id,
            "email": user.email,
            "last_login": user.last_login.isoformat() if user.last_login else None
        }
    }), 200

# CRUD de usuarios

@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

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

@api.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
