from algoritmo.utilidades_grafo import obtener_driver

def cargar_script_cypher(path):
    with open(path, "r", encoding="utf-8") as f:
        contenido = f.read()
    # Dividir por doble salto de línea (entre bloques)
    bloques = contenido.split("\n\n")
    return [bloque.strip() for bloque in bloques if bloque.strip() and not bloque.strip().startswith("//")]

def ejecutar_script(driver, bloques):
    with driver.session() as session:
        for bloque in bloques:
            try:
                session.run(bloque)
            except Exception as e:
                print(f"Error en bloque:\n{bloque}\n {e}")

if __name__ == "__main__":
    driver = obtener_driver()
    print("Ejecutando script Cypher de base...")
    bloques = cargar_script_cypher("datos_base/cargar_base.cypher")
    ejecutar_script(driver, bloques)
    print("Proceso finalizado.")


