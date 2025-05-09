CREATE (F:Categoria {nombre: "Fotografía"})
CREATE (D:Categoria {nombre: "Diseño Gráfico"})
CREATE (E:Categoria {nombre: "Escritura Creativa"})
CREATE (M:Categoria {nombre: "Música"})


CREATE (F1:Curso {titulo: "fotos1"})
CREATE (F2:Curso {titulo: "fotos2"})
CREATE (F3:Curso {titulo: "fotos3"})
CREATE (F1)-[:PERTENECE_A]->(F)
CREATE (F2)-[:PERTENECE_A]->(F)
CREATE (F3)-[:PERTENECE_A]->(F)

CREATE (D1:Curso {titulo: "diseño1"})
CREATE (D2:Curso {titulo: "diseño2"})
CREATE (D3:Curso {titulo: "diseño3"})
CREATE (D1)-[:PERTENECE_A]->(D)
CREATE (D2)-[:PERTENECE_A]->(D)
CREATE (D3)-[:PERTENECE_A]->(D)

CREATE (E1:Curso {titulo: "escritura1"})
CREATE (E2:Curso {titulo: "escritura2"})
CREATE (E3:Curso {titulo: "escritura3"})
CREATE (E1)-[:PERTENECE_A]->(E)
CREATE (E2)-[:PERTENECE_A]->(E)
CREATE (E3)-[:PERTENECE_A]->(E)

CREATE (M1:Curso {titulo: "musica1"})
CREATE (M2:Curso {titulo: "musica2"})
CREATE (M3:Curso {titulo: "musica3"})
CREATE (M1)-[:PERTENECE_A]->(M)
CREATE (M2)-[:PERTENECE_A]->(M)
CREATE (M3)-[:PERTENECE_A]->(M)

CREATE (juan:Usuario {nombre: "Juanito"})
CREATE (mar:Usuario {nombre: "Mar"})
CREATE (fran:Usuario {nombre: "Francisco"})

CREATE (juan)-[:INTERESADO_EN]->(F)
CREATE (juan)-[:INTERESADO_EN]->(M)

CREATE (mar)-[:INTERESADO_EN]->(D)
CREATE (mar)-[:INTERESADO_EN]->(E)

CREATE (fran)-[:INTERESADO_EN]->(M)
CREATE (fran)-[:INTERESADO_EN]->(E)


CREATE (F)-[:SIMILAR {peso: 4}]->(E)
CREATE (E)-[:SIMILAR {peso: 4}]->(F)

CREATE (F)-[:SIMILAR {peso: 4}]->(D)
CREATE (D)-[:SIMILAR {peso: 4}]->(F)

CREATE (F)-[:SIMILAR {peso: 2}]->(M)
CREATE (M)-[:SIMILAR {peso: 2}]->(F)

CREATE (E)-[:SIMILAR {peso: 3}]->(M)
CREATE (M)-[:SIMILAR {peso: 3}]->(E)

CREATE (E)-[:SIMILAR {peso: 2}]->(D)
CREATE (D)-[:SIMILAR {peso: 2}]->(E)

CREATE (M)-[:SIMILAR {peso: 2}]->(D)
CREATE (D)-[:SIMILAR {peso: 2}]->(M)
