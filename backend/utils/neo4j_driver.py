from neo4j import GraphDatabase

# URI de conexión a Aura
URI = "neo4j+s://1d3d3e94.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww"

# Devuelve una instancia del driver de Neo4j
def get_driver():
    return GraphDatabase.driver(URI, auth=(USER, PASSWORD))
