// Crear Categorías
MERGE (:Categoria {nombre: "Fotografía"});
MERGE (:Categoria {nombre: "Diseño Gráfico"});

// Crear Autores
MERGE (a1:Autor {id: "a1", nombre: "Laura Gómez", bio: "Fotógrafa profesional con 10 años de experiencia.", foto: "url_autor1"});
MERGE (a2:Autor {id: "a2", nombre: "Pedro Ruiz", bio: "Diseñador UX/UI y animador digital.", foto: "url_autor2"});

// Crear Cursos y relacionarlos
MERGE (c1:Curso {id: "F1", titulo: "Fotografía Digital para Principiantes", dificultad: "Básico", duracion: "4h", contenido: "Aprende los fundamentos de la fotografía digital.", foto: "url_foto_f1"})
MERGE (cat1:Categoria {nombre: "Fotografía"})
MERGE (a1:Autor {id: "a1"})
MERGE (c1)-[:PERTENECE_A]->(cat1)
MERGE (a1)-[:IMPARTE]->(c1)

MERGE (c2:Curso {id: "D1", titulo: "Diseño Gráfico con Illustrator", dificultad: "Intermedio", duracion: "6h", contenido: "Domina herramientas de diseño vectorial.", foto: "url_foto_d1"})
MERGE (cat2:Categoria {nombre: "Diseño Gráfico"})
MERGE (a2:Autor {id: "a2"})
MERGE (c2)-[:PERTENECE_A]->(cat2)
MERGE (a2)-[:IMPARTE]->(c2)
