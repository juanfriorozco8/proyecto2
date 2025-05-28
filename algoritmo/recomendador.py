from utilidades_grafo import ConexionNeo4j

class RecomendadorCursos:
    def __init__(self, conexion):
        self.db = conexion

    def recomendar_para_usuario(self, username, limite=5):
        """
        Recomendaciones personalizadas para un usuario según sus intereses.
        Excluye cursos ya inscritos por el usuario.
        """
        query = """
        MATCH (u:Usuario {username: $username})-[:TIENE_INTERES]->(i:Interes)<-[:TIENE_INTERES]-(c:Curso)
        WHERE NOT (u)-[:INSCRITO_EN]->(c)
        RETURN c.titulo AS titulo, c.categoria AS categoria, c.rating AS rating
        ORDER BY c.rating DESC
        LIMIT $limite
        """
        resultado = self.db.ejecutar_consulta(query, {"username": username, "limite": limite})
        return [registro.data() for registro in resultado]
