document.addEventListener("DOMContentLoaded", async () => {
  const usuario = localStorage.getItem("usuario");
  const cursosContainer = document.getElementById("cursos");
  const mensaje = document.getElementById("mensaje");

  if (!usuario) {
    mensaje.textContent = "No has iniciado sesión.";
    return;
  }

  try {
    const res = await fetch("/api/feed", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario }),
    });

    const cursos = await res.json();

    if (res.ok && cursos.length > 0) {
      cursos.forEach((curso) => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `
          <img src="${curso.foto || "https://via.placeholder.com/150"}" alt="${curso.titulo}" />
          <h3>${curso.titulo}</h3>
          <p><strong>Categoría:</strong> ${curso.categoria}</p>
          <p><strong>Dificultad:</strong> ${curso.dificultad}</p>
          <p><strong>Duración:</strong> ${curso.duracion}</p>
          <button onclick="verCurso('${curso.id}')">Ver más</button>
        `;
        cursosContainer.appendChild(div);
      });
    } else {
      mensaje.textContent = "No hay cursos recomendados en este momento.";
    }
  } catch (err) {
    console.error(err);
    mensaje.textContent = "Error al cargar cursos.";
  }
});

function verCurso(id) {
  localStorage.setItem("curso_id", id);
  window.location.href = "curso";
}
