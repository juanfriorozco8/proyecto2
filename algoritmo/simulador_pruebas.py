# algoritmo/simulador_pruebas.py

from utilidades_grafo import Neo4jConnector
from recomendador import recomendar_cursos

def main():
    # Configura tu conexión a Neo4j
    neo4j = Neo4jConnector(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"  # cámbialo si es necesario
    )

    # ID del usuario a testear
    usuario_id = "u1"  # debe existir en la base con nodos conectados

    print(f"\n🔍 Recomendaciones para el usuario '{usuario_id}':\n")

    recomendaciones = recomendar_cursos(neo4j, usuario_id)

    if recomendaciones:
        for r in recomendaciones:
            print(f"📚 {r['titulo']} — Score: {round(r['score_total'], 2)}")
    else:
        print("⚠️ No se encontraron recomendaciones. Verifica los datos.")

    # Cerrar conexión
    neo4j.cerrar()

if __name__ == "__main__":
    main()
