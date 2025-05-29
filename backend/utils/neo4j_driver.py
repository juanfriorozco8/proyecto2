import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Cargar las variables del archivo .env para proteger la información de la base de datos
load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

def get_driver():
    return GraphDatabase.driver(URI, auth=(USER, PASSWORD))

