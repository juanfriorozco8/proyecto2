from relaciones_interacciones.registrar_interaccion import registrar_interacciones
from algoritmo.recomendador import recomendar_cursos

def main():
    registrar_interacciones()
    recomendaciones = recomendar_cursos("mari123")
    print("Cursos recomendados para mari123:")
    for r in recomendaciones:
        print(f"- {r['titulo']} ({r['duracion']})")

if __name__ == "__main__":
    main()