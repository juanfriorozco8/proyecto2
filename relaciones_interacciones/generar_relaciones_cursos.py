from algoritmo.utilidades_grafo import get_driver

def generar_relaciones_similares():
    driver = get_driver()
    with driver.session() as session:
        # Relacionar cursos con mismo autor
        session.run("""
        MATCH (a:Autor)-[:CREO]->(c1:Curso), (a)-[:CREO]->(c2:Curso)
        WHERE c1 <> c2
        MERGE (c1)-[:MISMO_AUTOR]->(c2)
        """)

        # Relacionar cursos con misma dificultad
        session.run("""
        MATCH (c1:Curso), (c2:Curso)
        WHERE c1.dificultad = c2.dificultad AND c1 <> c2
        MERGE (c1)-[:SIMILAR_DIFICULTAD]->(c2)
        """)

        # Relacionar cursos con duración similar (±1 hora)
        session.run("""
        MATCH (c1:Curso), (c2:Curso)
        WHERE c1 <> c2
          AND toInteger(REPLACE(c1.duracion, 'h', '')) >= toInteger(REPLACE(c2.duracion, 'h', '')) - 1
          AND toInteger(REPLACE(c1.duracion, 'h', '')) <= toInteger(REPLACE(c2.duracion, 'h', '')) + 1
        MERGE (c1)-[:DURACION_SIMILAR]->(c2)
        """)

        print("✅ Relaciones entre cursos generadas correctamente.")

if __name__ == "__main__":
    generar_relaciones_similares()