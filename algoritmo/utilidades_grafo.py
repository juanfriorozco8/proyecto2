# algoritmo/utilidades_grafo.py

from neo4j import GraphDatabase

class Neo4jConnector:
    def __init__(self, uri="neo4j+s://1d3d3e94.databases.neo4j.io", user="neo4j", password="vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def cerrar(self):
        if self.driver:
            self.driver.close()

    def ejecutar_query(self, query, parameters=None):
        parameters = parameters or {}
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def ejecutar_con_funcion(self, funcion, **kwargs):
        with self.driver.session() as session:
            return funcion(session, **kwargs)
