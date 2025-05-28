from algoritmo.utilidades_grafo import obtener_driver

def cargar_script_cypher(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ejecutar_script(driver, script):
    with driver.session() as session:
        session.run(script)

if __name__ == "__main__":
    driver = obtener_driver()
    print("Ejecutando script Cypher de base...")
    script = cargar_script_cypher("datos_base/cargar_base.cypher")
    ejecutar_script(driver, script)
    print("Base de datos cargada con éxito.")
