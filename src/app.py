"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from api.utils import APIException, generate_sitemap
from api.models import db, User
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from api.login import login_bp
from api.profile import profile_bp

# Configuración de la aplicación Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Registrar Blueprints
app.register_blueprint(profile_bp, url_prefix='/private')
app.register_blueprint(login_bp, url_prefix='/login')

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'any key works'

# Inicializar la base de datos y migraciones
db.init_app(app)
MIGRATE = Migrate(app, db, compare_type=True)
jwt = JWTManager(app)

# Agregar las rutas y administradores
setup_admin(app)
setup_commands(app)
app.register_blueprint(api, url_prefix='/api')

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar sitemap
@app.route('/')
def sitemap():
    ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
    if ENV == "development":
        return generate_sitemap(app)
    static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
    return send_from_directory(static_file_dir, 'index.html')

# Manejar cualquier otra ruta como archivo estático
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # Evitar caché
    return response

@app.route('/api/hello', methods=['GET', 'OPTIONS'])
def handle_hello():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200  # Responder a solicitudes preflight
    response_body = {
        "message": "Hello! I'm a message that came from the backend."
    }
    return jsonify(response_body), 200


# Rutas de autenticación
@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Lógica de autenticación básica
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user": {"id": user.id, "email": user.email}}), 200

# Rutas protegidas
@app.route('/api/user/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize()), 200

# Agregar encabezados de CORS para las respuestas
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'  # Sólo una vez
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


# Iniciar la aplicación
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
