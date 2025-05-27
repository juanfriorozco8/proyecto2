// Crear categorías
MERGE (:Categoria {nombre: "Fotografía"})
MERGE (:Categoria {nombre: "Diseño Gráfico"})

// Crear autores y cursos
MERGE (a1:Autor {id: "A1", nombre: "Laura Gómez", bio: "Fotógrafa profesional con 10 años de experiencia.", foto: "laura.jpg"})
MERGE (a2:Autor {id: "A2", nombre: "Pedro Ruiz", bio: "Diseñador UX/UI y animador digital.", foto: "pedro.jpg"})

MERGE (c1:Curso {id: "CURS001", titulo: "Fotografía Creativa", categoria: "Fotografía", dificultad: "Intermedio", duracion: "6h", contenido: "Técnicas de iluminación, composición y edición.", fotos: ["fotografia1.jpg", "fotografia2.jpg"]})
MERGE (c2:Curso {id: "CURS002", titulo: "Diseño Gráfico Básico", categoria: "Diseño Gráfico", dificultad: "Principiante", duracion: "5h", contenido: "Fundamentos de color, tipografía y herramientas de diseño.", fotos: ["diseno1.jpg"]})

// Relación autor → curso
WITH a1, a2, c1, c2
MERGE (a1)-[:CREO]->(c1)
MERGE (a2)-[:CREO]->(c2)

// Crear categorías
MERGE (cat1:Categoria {nombre: "Fotografía"})
MERGE (cat2:Categoria {nombre: "Diseño Gráfico"})

// Relación curso → categoría
WITH c1, c2, cat1, cat2
MERGE (c1)-[:PERTENECE_A]->(cat1)
MERGE (c2)-[:PERTENECE_A]->(cat2)


