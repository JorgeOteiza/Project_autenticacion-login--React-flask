import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from api.utils import generate_sitemap
from api.models import db
from api.routes import api  # Único Blueprint para las rutas de la API
from api.admin import setup_admin
from api.commands import setup_commands
from api.login import login_bp  # Blueprint para login

app = Flask(__name__)

# Configuración de la base de datos y JWT
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev_secret_key')

db.init_app(app)
Migrate(app, db, compare_type=True)
jwt = JWTManager(app)

# Configuración de CORS
CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGIN", "https://petrifying-spooky-poltergeist-7v97v6w49rqgcp57v-3000.app.github.dev")}}, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Registrar Blueprints y comandos
setup_admin(app)
setup_commands(app)
app.register_blueprint(api, url_prefix='/api')     # Blueprint consolidado para todas las rutas de la API
app.register_blueprint(login_bp, url_prefix='/login')  # Blueprint para login

# Manejo de errores y Sitemap (sin cambios)
@app.errorhandler(Exception)
def handle_exception(e):
    response = {"message": "An error occurred", "error": str(e)}
    return jsonify(response), 500

@app.route('/')
def sitemap():
    ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
    if ENV == "development":
        return generate_sitemap(app)
    static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
    return send_from_directory(static_file_dir, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    return send_from_directory(static_file_dir, path)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
