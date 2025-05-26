
MATCH (u:Usuario {usuario: $usuario})
MATCH (u)-[:INTERESADO_EN]->(cat1:Categoria)
OPTIONAL MATCH (cat1)-[sim:SIMILAR]->(cat2:Categoria)
WITH u, cat1, collect(DISTINCT cat2) + cat1 AS categoriasRelevantes
UNWIND categoriasRelevantes AS cat
MATCH (c:Curso)-[:PERTENECE_A]->(cat)
WHERE NOT (u)-[:TOMO]->(c)
OPTIONAL MATCH (c)<-[:TOMO]-(otros:Usuario)
WITH u, c, COUNT(otros) AS popularidad
OPTIONAL MATCH (c)<-[:IMPARTIO]-(a:Autor)<-[:IMPARTIO]-(:Curso)<-[:TOMO]-(u)
WITH u, c, popularidad,
     CASE WHEN a IS NOT NULL THEN 1 ELSE 0 END AS autorCoincide,
     c.rating AS rating,
     ABS(c.dificultad - u.nivel_deseado) AS diff_dif
OPTIONAL MATCH (u)-[:INTERESADO_EN]->(catS:Categoria)<-[:INTERESADO_EN]-(sim:Usuario)-[:TOMO]->(c)
WITH u, c, popularidad, autorCoincide, rating, diff_dif, COUNT(DISTINCT sim) AS similares
WITH c,
     (CASE WHEN diff_dif = 0 THEN 1 ELSE 0 END +
      autorCoincide * 2 +
      rating +
      popularidad / 100 +
      similares * 1.5) AS score
RETURN c.titulo AS curso, score
ORDER BY score DESC
LIMIT 10