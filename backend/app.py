""" from flask import Flask
from rutas import curso, index, register, login, feed
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecreto")

# Registrar Blueprints
app.register_blueprint(index.index_bp)
app.register_blueprint(register.register_bp)
app.register_blueprint(login.login_bp)
app.register_blueprint(feed.feed_bp)
app.register_blueprint(curso.curso_bp)

if __name__ == "__main__":
    app.run(debug=True)
 """
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from flask import Flask
from dotenv import load_dotenv
import os
from backend.rutas import blueprints

load_dotenv()

app = Flask(__name__, template_folder="./templates")
app.secret_key = os.getenv("SECRET_KEY", "supersecreto")

# Registrar todos los blueprints
for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)