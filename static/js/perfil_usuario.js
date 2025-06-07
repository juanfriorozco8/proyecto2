document.addEventListener("DOMContentLoaded", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const usuario = urlParams.get("usuario") || sessionStorage.getItem("perfil_usuario");
    const nombreUsuario = document.getElementById("nombre-usuario");
    const interesesContainer = document.getElementById("intereses");
    const cursosContainer = document.getElementById("cursos");
    const mensaje = document.getElementById("mensaje");

    if (!usuario) {
        mensaje.textContent = "No se especificó usuario.";
        console.error("No se encontró usuario");
        return;
    }

    try {
        const res = await fetch("/api/perfil_usuario", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario })
        });

        const data = await res.json();
        console.log("Datos del perfil:", data);

        if (res.ok) {
            nombreUsuario.textContent = data.usuario;
            
            // Intereses
            if (data.intereses.length > 0) {
                data.intereses.forEach(interes => {
                    const div = document.createElement("div");
                    div.className = "card";
                    div.innerHTML = `<h3>${interes}</h3>`;
                    interesesContainer.appendChild(div);
                });
            } else {
                interesesContainer.innerHTML = "<p>No hay intereses registrados.</p>";
            }

            // Cursos
            if (data.cursos.length > 0) {
                data.cursos.forEach(curso => {
                    const div = document.createElement("div");
                    div.className = "card";
                    div.innerHTML = `
                        <h3>${curso.titulo}</h3>
                        <p><strong>Categoría:</strong> ${curso.categoria}</p>
                        <p><strong>Calificación:</strong> ${curso.calificacion}</p>
                        <button class="next" onclick="verCurso('${curso.id}')">Ver curso</button>
                    `;
                    cursosContainer.appendChild(div);
                });
            } else {
                cursosContainer.innerHTML = "<p>No hay cursos realizados.</p>";
            }
        } else {
            mensaje.textContent = data.error || "Error al cargar el perfil.";
            console.log("Respuesta no OK:", data);
        }
    } catch (err) {
        mensaje.textContent = "Error al cargar el perfil.";
        console.error("Error:", err);
    }
});

function verCurso(id) {
    sessionStorage.setItem("curso_id", id);
    window.location.href = `/curso?id=${id}`;
}