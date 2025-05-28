// Script base para crear nodos
CREATE (f:Categoria {nombre: "Fotografía"});
CREATE (d:Categoria {nombre: "Diseño Gráfico"});

CREATE (a1:Autor {id: "A1", nombre: "Laura Gómez", bio: "Fotógrafa profesional", foto: "laura.jpg"});
CREATE (a2:Autor {id: "A2", nombre: "Pedro Ruiz", bio: "Diseñador UX/UI", foto: "pedro.jpg"});

CREATE (c1:Curso {id: "C1", titulo: "Fotografía Digital", dificultad: "Intermedio", duracion: "5h", contenido: "Aprende fotografía", fotos: ["foto1.jpg", "foto2.jpg"]});
CREATE (c2:Curso {id: "C2", titulo: "Diseño UX/UI", dificultad: "Avanzado", duracion: "8h", contenido: "Diseña interfaces", fotos: ["ux1.jpg", "ux2.jpg"]});

MATCH (c:Curso {id: "C1"}), (a:Autor {id: "A1"}), (cat:Categoria {nombre: "Fotografía"})
CREATE (a)-[:CREO]->(c)
CREATE (c)-[:PERTENECE_A]->(cat);

MATCH (c:Curso {id: "C2"}), (a:Autor {id: "A2"}), (cat:Categoria {nombre: "Diseño Gráfico"})
CREATE (a)-[:CREO]->(c)
CREATE (c)-[:PERTENECE_A]->(cat);