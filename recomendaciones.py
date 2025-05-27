from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from py2neo import Graph, Node, Relationship
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Habilitar CORS para frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar a Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# ---------------------- MODELOS ----------------------
class UsuarioInput(BaseModel):
    usuario: str
    contraseña: str
    email: str
    nivel_deseado: int

class Curso(BaseModel):
    idCurso: str
    titulo: str
    duracion: str
    dificultad: int
    contenido: str
    categoria: str
    autor: str
    fotoPresentacion: str
    fotos: list[str]
    popularidad: int
    rating: float

# ---------------------- ENDPOINTS ----------------------
@app.post("/usuario")
def crear_usuario(data: UsuarioInput):
    query = """
    MERGE (u:Usuario {usuario: $usuario})
    SET u.email = $email, u.contraseña = $contraseña, u.nivel_deseado = $nivel
    """
    graph.run(query, 
        usuario=data.usuario, 
        email=data.email, 
        contraseña=data.contraseña,
        nivel=data.nivel_deseado
    )
    return {"mensaje": "Usuario creado o actualizado"}

@app.get("/cursos")
def obtener_cursos_por_categoria(categoria: str):
    query = """
    MATCH (c:Categoria {nombre: $categoria})<-[:PERTENECE_A]-(curso:Curso)
    RETURN curso
    """
    result = graph.run(query, categoria=categoria)
    cursos = [record["curso"] for record in result]
    return cursos

@app.get("/recomendaciones_usuario")
def recomendaciones_usuario(usuario: str):
    query = """
    MATCH (u:Usuario {usuario: $usuario})-[:INTERESADO_EN]->(cat:Categoria)<-[:PERTENECE_A]-(c:Curso)
    RETURN DISTINCT c ORDER BY c.popularidad DESC LIMIT 5
    """
    result = graph.run(query, usuario=usuario)
    recomendaciones = [record["c"] for record in result]
    return recomendaciones
