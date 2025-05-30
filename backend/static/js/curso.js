document.addEventListener("DOMContentLoaded", async () => {
  const cursoId = localStorage.getItem("curso_id");
  const usuario = localStorage.getItem("usuario");
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
      document.getElementById("autorNombre").textContent = curso.autor.nombre;
      document.getElementById("autorBio").textContent = curso.autor.bio;
      document.getElementById("autorFoto").src = curso.autor.foto || "";
    } else {
      mensaje.textContent = "Curso no encontrado.";
    }
  } catch (err) {
    console.error(err);
    mensaje.textContent = "Error al cargar el curso.";
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

async function calificar(valor) {
  const cursoId = localStorage.getItem("curso_id");
  const usuario = localStorage.getItem("usuario");
  const mensaje = document.getElementById("mensaje");

  try {
    const res = await fetch("/api/rating", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario, curso_id: cursoId, rating: valor }),
    });

    const json = await res.json();
    mensaje.textContent = res.ok ? "¡Gracias por tu calificación!" : json.error;
    mensaje.style.color = res.ok ? "green" : "red";
  } catch (err) {
    mensaje.textContent = "Error al calificar.";
    console.error(err);
  }
}
