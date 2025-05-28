from neo4j import GraphDatabase

URI = "neo4j+s://1d3d3e94.databases.neo4j.io"
AUTH = ("neo4j", "vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww")

driver = GraphDatabase.driver(URI, auth=AUTH)

with driver.session() as session:
    # Crear un nodo temporal
    session.run("MERGE (:Testeo {mensaje: '¡Hola Aura desde Python!'})")
    print("✅ Nodo de prueba creado en Neo4j Aura.")

    # Verificar si existe
    result = session.run("MATCH (t:Testeo) RETURN t.mensaje AS mensaje")
    for r in result:
        print("🔍 Nodo leído desde Aura:", r["mensaje"])
