from flask import Flask
from flask_cors import CORS

# Importación de los blueprints de las rutas
from backend.rutas.login import login_bp
from backend.rutas.register import register_bp
from backend.rutas.feed import feed_bp
from backend.rutas.curso import curso_bp

# Creación de la aplicación Flask
app = Flask(__name__)

# Se habilita CORS para permitir peticiones desde el frontend
CORS(app)

# Se registran los blueprints con prefijo '/api'
app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(register_bp, url_prefix='/api')
app.register_blueprint(feed_bp, url_prefix='/api')
app.register_blueprint(curso_bp, url_prefix='/api')

# Ejecuta la app en modo debug para desarrollo local
if __name__ == '__main__':
    app.run(debug=True, port=5050)

