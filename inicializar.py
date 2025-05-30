import os

# Ejecutar carga de cursos y autores
print("\n Cargando base de cursos y autores...")
os.system("python -m datos_base.cargar_base")

# Generar relaciones entre cursos similares
print("\n Generando relaciones entre cursos similares...")
os.system("python -m relaciones_interacciones.generar_relaciones_cursos")

# Registrar usuarios simulados e intereses
print("\n Registrando usuarios e intereses...")
os.system("python -m relaciones_interacciones.registrar_interaccion")

# Simular interacciones
print("\\n Simulando interacciones para 'mari123'...")
os.system("python -m relaciones_interacciones.simular_interacciones")

# Ejecutar recomendador para prueba
print("\n Ejecutando recomendaciones para 'mari123'...")
os.system("python -m algoritmo.simulador_pruebas")

