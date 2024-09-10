import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api  # Importa el Blueprint con las rutas
from api.admin import setup_admin
from api.commands import setup_commands
from api.login import login_bp

# Configuración de la aplicación Flask
app = Flask(__name__)

# Habilitar CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

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
Migrate(app, db, compare_type=True)
jwt = JWTManager(app)

# Registrar Blueprints y comandos
setup_admin(app)
setup_commands(app)
app.register_blueprint(api, url_prefix='/api')  # Registro de rutas
app.register_blueprint(login_bp, url_prefix='/login')  # Registra el blueprint del login



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

# Iniciar la aplicación
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
