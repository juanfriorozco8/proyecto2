
// BASE DE DATOS: CATEGORÍAS, AUTORES, CURSOS, USUARIOS, RELACIONES

CREATE (F:Categoria {nombre: "Fotografía"})
CREATE (D:Categoria {nombre: "Diseño Gráfico"})
CREATE (E:Categoria {nombre: "Escritura Creativa"})
CREATE (M:Categoria {nombre: "Música"})

CREATE (a1:Autor {nombre: "Laura Gómez", bio: "Fotógrafa profesional con 10 años de experiencia", foto: "url_autor1"})
CREATE (a2:Autor {nombre: "Pedro Ruiz", bio: "Diseñador UX/UI y animador digital", foto: "url_autor2"})
CREATE (a3:Autor {nombre: "María Torres", bio: "Escritora y guionista", foto: "url_autor3"})
CREATE (a4:Autor {nombre: "Carlos Méndez", bio: "Músico profesional y compositor", foto: "url_autor4"})

// CURSOS DE FOTOGRAFÍA
CREATE (F1:Curso {idCurso: "F1", titulo: "fotos1", duracion: "4h", dificultad: 2, contenido: "Luz natural, encuadre, exposición", fotoPresentacion: "url_foto1", acercaAutor: "Laura Gómez", fotos: ["img1", "img2"], fotoAutor: "url_autor1", popularidad: 120, rating: 4.6})-[:PERTENECE_A]->(F)
CREATE (F2:Curso {idCurso: "F2", titulo: "fotos2", duracion: "5h", dificultad: 1, contenido: "Composición básica", fotoPresentacion: "url_foto2", acercaAutor: "Laura Gómez", fotos: ["img3"], fotoAutor: "url_autor1", popularidad: 80, rating: 4.2})-[:PERTENECE_A]->(F)
CREATE (F3:Curso {idCurso: "F3", titulo: "fotos3", duracion: "6h", dificultad: 3, contenido: "Técnicas avanzadas", fotoPresentacion: "url_foto3", acercaAutor: "Laura Gómez", fotos: ["img4"], fotoAutor: "url_autor1", popularidad: 200, rating: 4.9})-[:PERTENECE_A]->(F)
CREATE (a1)-[:IMPARTIO]->(F1)
CREATE (a1)-[:IMPARTIO]->(F2)
CREATE (a1)-[:IMPARTIO]->(F3)

// CURSOS DE DISEÑO GRÁFICO
CREATE (D1:Curso {idCurso: "D1", titulo: "diseño1", duracion: "3h", dificultad: 2, contenido: "Adobe Illustrator", fotoPresentacion: "url_d1", acercaAutor: "Pedro Ruiz", fotos: [], fotoAutor: "url_autor2", popularidad: 140, rating: 4.3})-[:PERTENECE_A]->(D)
CREATE (D2:Curso {idCurso: "D2", titulo: "diseño2", duracion: "5h", dificultad: 1, contenido: "Diseño para principiantes", fotoPresentacion: "url_d2", acercaAutor: "Pedro Ruiz", fotos: [], fotoAutor: "url_autor2", popularidad: 95, rating: 4.0})-[:PERTENECE_A]->(D)
CREATE (D3:Curso {idCurso: "D3", titulo: "diseño3", duracion: "6h", dificultad: 3, contenido: "Animación digital", fotoPresentacion: "url_d3", acercaAutor: "Pedro Ruiz", fotos: [], fotoAutor: "url_autor2", popularidad: 180, rating: 4.8})-[:PERTENECE_A]->(D)
CREATE (a2)-[:IMPARTIO]->(D1)
CREATE (a2)-[:IMPARTIO]->(D2)
CREATE (a2)-[:IMPARTIO]->(D3)

// CURSOS DE ESCRITURA
CREATE (E1:Curso {idCurso: "E1", titulo: "escritura1", duracion: "2h", dificultad: 1, contenido: "Relato corto", fotoPresentacion: "url_e1", acercaAutor: "María Torres", fotos: [], fotoAutor: "url_autor3", popularidad: 75, rating: 4.1})-[:PERTENECE_A]->(E)
CREATE (E2:Curso {idCurso: "E2", titulo: "escritura2", duracion: "4h", dificultad: 2, contenido: "Narrativa visual", fotoPresentacion: "url_e2", acercaAutor: "María Torres", fotos: [], fotoAutor: "url_autor3", popularidad: 110, rating: 4.5})-[:PERTENECE_A]->(E)
CREATE (E3:Curso {idCurso: "E3", titulo: "escritura3", duracion: "5h", dificultad: 3, contenido: "Novela", fotoPresentacion: "url_e3", acercaAutor: "María Torres", fotos: [], fotoAutor: "url_autor3", popularidad: 170, rating: 4.7})-[:PERTENECE_A]->(E)
CREATE (a3)-[:IMPARTIO]->(E1)
CREATE (a3)-[:IMPARTIO]->(E2)
CREATE (a3)-[:IMPARTIO]->(E3)

// CURSOS DE MÚSICA
CREATE (M1:Curso {idCurso: "M1", titulo: "musica1", duracion: "2h", dificultad: 1, contenido: "Introducción al piano", fotoPresentacion: "url_m1", acercaAutor: "Carlos Méndez", fotos: [], fotoAutor: "url_autor4", popularidad: 90, rating: 4.4})-[:PERTENECE_A]->(M)
CREATE (M2:Curso {idCurso: "M2", titulo: "musica2", duracion: "3h", dificultad: 2, contenido: "Improvisación musical", fotoPresentacion: "url_m2", acercaAutor: "Carlos Méndez", fotos: [], fotoAutor: "url_autor4", popularidad: 100, rating: 4.6})-[:PERTENECE_A]->(M)
CREATE (M3:Curso {idCurso: "M3", titulo: "musica3", duracion: "4h", dificultad: 3, contenido: "Composición avanzada", fotoPresentacion: "url_m3", acercaAutor: "Carlos Méndez", fotos: [], fotoAutor: "url_autor4", popularidad: 160, rating: 4.9})-[:PERTENECE_A]->(M)
CREATE (a4)-[:IMPARTIO]->(M1)
CREATE (a4)-[:IMPARTIO]->(M2)
CREATE (a4)-[:IMPARTIO]->(M3)

// USUARIOS
CREATE (juan:Usuario {usuario: "juanito", contraseña: "1234", email: "juan@example.com", nivel_deseado: 2})
CREATE (mar:Usuario {usuario: "mar", contraseña: "abcd", email: "mar@example.com", nivel_deseado: 1})
CREATE (fran:Usuario {usuario: "fran", contraseña: "pass", email: "fran@example.com", nivel_deseado: 3})

// INTERESES Y CURSOS TOMADOS
CREATE (juan)-[:INTERESADO_EN]->(F)
CREATE (juan)-[:INTERESADO_EN]->(M)
CREATE (juan)-[:TOMO]->(F1)
CREATE (mar)-[:INTERESADO_EN]->(D)
CREATE (mar)-[:INTERESADO_EN]->(E)
CREATE (mar)-[:TOMO]->(D1)
CREATE (fran)-[:INTERESADO_EN]->(M)
CREATE (fran)-[:INTERESADO_EN]->(E)
CREATE (fran)-[:TOMO]->(E1)

// RELACIONES ENTRE CATEGORÍAS
CREATE (F)-[:SIMILAR {peso: 4}]->(E)
CREATE (F)-[:SIMILAR {peso: 4}]->(D)
CREATE (F)-[:SIMILAR {peso: 2}]->(M)
CREATE (E)-[:SIMILAR {peso: 3}]->(M)
CREATE (E)-[:SIMILAR {peso: 2}]->(D)
CREATE (M)-[:SIMILAR {peso: 2}]->(D)

// 📌 CURSOS NUEVOS EN FOTOGRAFÍA Y MÚSICA PARA RECOMENDAR A JUANITO

// Curso nuevo que Juanito NO ha tomado pero está en categoría que le interesa
CREATE (F4:Curso {
  idCurso: "F4", 
  titulo: "Edición de fotos con Lightroom", 
  duracion: "3h", 
  dificultad: 2, 
  contenido: "Edición digital de fotografías", 
  fotoPresentacion: "url_foto4", 
  acercaAutor: "Laura Gómez", 
  fotos: ["img5"], 
  fotoAutor: "url_autor1", 
  popularidad: 95, 
  rating: 4.4
})-[:PERTENECE_A]->(F)
CREATE (a1)-[:IMPARTIO]->(F4)

// Curso nuevo en música que Juanito no ha tomado
CREATE (M4:Curso {
  idCurso: "M4", 
  titulo: "Grabación en estudio casero", 
  duracion: "2.5h", 
  dificultad: 2, 
  contenido: "Técnicas básicas de grabación", 
  fotoPresentacion: "url_m4", 
  acercaAutor: "Carlos Méndez", 
  fotos: [], 
  fotoAutor: "url_autor4", 
  popularidad: 88, 
  rating: 4.5
})-[:PERTENECE_A]->(M)
CREATE (a4)-[:IMPARTIO]->(M4)

// Simulamos que otros usuarios han tomado estos cursos, para darles popularidad
MATCH (mar:Usuario {usuario: "mar"}), (fran:Usuario {usuario: "fran"})
MATCH (c1:Curso {idCurso: "F4"}), (c2:Curso {idCurso: "M4"})
CREATE (mar)-[:TOMO]->(c1)
CREATE (fran)-[:TOMO]->(c2)
