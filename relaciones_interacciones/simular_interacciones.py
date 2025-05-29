from algoritmo.utilidades_grafo import get_driver

def simular_interacciones():
    driver = get_driver()
    with driver.session() as session:
        # Simular inscripción de mari123 al curso C1
        session.run("""
        MATCH (u:Usuario {username: 'mari123'}), (c:Curso {idCurso: 'C1'})
        MERGE (u)-[:INSCRITO_EN]->(c)
        """)

        # Simular like
        session.run("""
        MATCH (u:Usuario {username: 'mari123'}), (c:Curso {idCurso: 'C1'})
        MERGE (u)-[:DIO_LIKE]->(c)
        """)

        # Simular calificación
        session.run("""
        MATCH (u:Usuario {username: 'mari123'}), (c:Curso {idCurso: 'C1'})
        MERGE (u)-[r:CALIFICO]->(c)
        SET r.valor = 5
        """)

        print("✅ Interacciones simuladas para 'mari123' en curso 'C1'.")

if __name__ == "__main__":
    simular_interacciones()
