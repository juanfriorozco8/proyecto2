
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

print(f"DEBUG Neo4j URI: {NEO4J_URI}")
print(f"DEBUG Neo4j USER: {NEO4J_USER}")
print(f"DEBUG Neo4j PASSWORD: {NEO4J_PASSWORD}")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_driver():
    return driver



