from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "neo4j+s://1d3d3e94.databases.neo4j.io", 
    auth=("neo4j", "vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww")
)

with driver.session() as session:
    result = session.run("RETURN '🎉 Conexión exitosa a Aura' AS mensaje")
    print(result.single()["mensaje"])
