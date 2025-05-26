# main.py – Backend FastAPI + Neo4j Aura

from fastapi import FastAPI, Query
from neo4j import GraphDatabase
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir conexión desde el frontend (HTML, JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a tu base Aura (cambia los datos por los tuyos)
uri = "neo4j+s://1d3d3e94.databases.neo4j.io "
user = "neo4j"
password = "vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww"
driver = GraphDatabase.driver(uri, auth=(user, password))

# Cargar la consulta Cypher desde recomendaciones.cypher
def cargar_query():
    with open("recomendaciones.cypher", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/recomendar")
def recomendar(usuario: str = Query(...)):
    query = cargar_query()
    with driver.session() as session:
        result = session.run(query, usuario=usuario)
        return [{"curso": r["curso"], "score": r["score"]} for r in result]

