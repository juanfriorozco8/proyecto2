from algoritmo.utilidades_grafo import get_driver

def recomendar_cursos(usuario):
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            '''
            MATCH (u:Usuario {username: $usuario})-[:INTERESADO_EN]->(cat:Categoria)<-[:PERTENECE_A]-(c:Curso)
            RETURN c.titulo AS titulo, c.duracion AS duracion
            ''',
            usuario=usuario
        )
        return [record.data() for record in result]