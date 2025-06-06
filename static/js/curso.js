document.addEventListener("DOMContentLoaded", async () => {
  const cursoId = new URLSearchParams(window.location.search).get("id");
  const usuario = sessionStorage.getItem("usuario");
  const mensaje = document.getElementById("mensaje");

  if (!cursoId || !usuario) {
    mensaje.textContent = "No se encontró el curso o usuario.";
    return;
  }

  try {
    const res = await fetch(`/api/curso/${cursoId}`);
    const curso = await res.json();

    if (res.ok) {
      document.getElementById("tituloCurso").textContent = curso.titulo;
      document.getElementById("fotoCurso").src = curso.foto || "";
      document.getElementById("categoria").textContent = curso.categoria;
      document.getElementById("dificultad").textContent = curso.dificultad;
      document.getElementById("duracion").textContent = curso.duracion;
      document.getElementById("contenido").textContent = curso.contenido;

      const autorId = curso.impartido_por;
      if (autorId) {
        const resAutor = await fetch(`/api/autor/${autorId}`);
        const autor = await resAutor.json();

        if (resAutor.ok) {
          document.getElementById("autorNombre").textContent = autor.nombre;
          document.getElementById("autorBio").textContent = autor.bio;
          document.getElementById("autorFoto").src = autor.foto || "";
        }
      }
    } else {
      mensaje.textContent = "Curso no encontrado.";
    }
  } catch (err) {
    mensaje.textContent = "Error al cargar el curso.";
    console.error(err);
  }

  document.getElementById("btnInscribir").addEventListener("click", async () => {
    try {
      const res = await fetch("/api/inscribir", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, curso_id: cursoId }),
      });

      const json = await res.json();
      mensaje.textContent = res.ok ? "¡Inscrito con éxito!" : json.error;
      mensaje.style.color = res.ok ? "green" : "red";
    } catch (err) {
      mensaje.textContent = "Error al inscribirse.";
      console.error(err);
    }
  });
});
