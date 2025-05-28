from neo4j import GraphDatabase

class ConexionNeo4j:
    def __init__(self, uri, user, password):
        """
        Crea una conexión con la base de datos Neo4j.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def cerrar(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.driver.close()

    def ejecutar_consulta(self, consulta, parametros=None):
        """
        Ejecuta una consulta Cypher y devuelve los resultados.
        """
        with self.driver.session() as session:
            resultado = session.run(consulta, parametros or {})
            return resultado
