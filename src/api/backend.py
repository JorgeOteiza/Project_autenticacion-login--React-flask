from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from models import User

app = Flask(__name__)

# Configuración CORS para permitir solicitudes desde cualquier origen
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gitpod:postgres@localhost/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'any key works'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Aquí agrego las rutas, por ej:
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user": {"id": user.id, "email": user.email}}), 200

@app.route('/api/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize()), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
