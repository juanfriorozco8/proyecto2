from utilidades_grafo import ConexionNeo4j
from recomendador import RecomendadorCursos

def main():
    uri = "neo4j+s://1d3d3e94.databases.neo4j.io"
    user = "<neo4j>"
    password = "<vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww>"

    conexion = ConexionNeo4j(uri, user, password)

    try:
        recomendador = RecomendadorCursos(conexion)
        username = input("🔑 Ingresa el nombre de usuario: ")
        recomendaciones = recomendador.recomendar_para_usuario(username)

        if recomendaciones:
            print(f"\n Recomendaciones para {username}:")
            for curso in recomendaciones:
                print(f"- {curso['titulo']} | Categoría: {curso['categoria']} |  {curso['rating']}")
        else:
            print( "No se encontraron cursos recomendados.")
    finally:
        conexion.cerrar()

if __name__ == "__main__":
    main()
