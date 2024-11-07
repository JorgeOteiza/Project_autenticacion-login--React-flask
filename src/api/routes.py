from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import db, User

api = Blueprint('api', __name__)

# Ruta de saludo
@api.route('/hello', methods=['GET'])
def handle_hello():
    return jsonify({"message": "Hello! I'm a message from the backend."}), 200

# Ruta para registro de usuarios
@api.route('/signup', methods=['POST'])
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

    token = create_access_token(identity=new_user.id)
    return jsonify({
        "message": "User created successfully!",
        "user": {"id": new_user.id, "email": new_user.email},
        "token": token
    }), 201

# Ruta de login
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"token": token, "user": user.serialize()}), 200

# Ruta protegida para obtener el perfil del usuario actual
@api.route('/profile/<int:id>', methods=['GET'])
@jwt_required()
def get_profile(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user and user.id == id:
        return jsonify(user.serialize())
    else:
        return jsonify({"message": "User not found or unauthorized"}), 404

# Ruta protegida para acceder a todos los usuarios (requiere autenticación)
@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# Ruta para obtener, actualizar y eliminar un usuario específico
@api.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def manage_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if request.method == 'GET':
        return jsonify(user.serialize())

    data = request.get_json()
    if request.method == 'PUT':
        email = data.get('email')
        password = data.get('password')
        if email:
            user.email = email
        if password:
            user.set_password(password)
        db.session.commit()
        return jsonify(user.serialize()), 200

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200

# Ruta para actualizar el perfil del usuario actual
@api.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
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

# Ruta para eliminar la cuenta del usuario actual
@api.route('/delete_account', methods=['DELETE'])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 200
