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
            document.getElementById("fotoCurso").src = curso.foto || "https://via.placeholder.com/150";
            document.getElementById("categoria").textContent = curso.categoria;
            document.getElementById("dificultad").textContent = curso.dificultad;
            document.getElementById("duracion").textContent = curso.duracion;
            document.getElementById("contenido").textContent = curso.contenido;
            document.getElementById("autorNombre").textContent = curso.autor.nombre;
            document.getElementById("autorBio").textContent = curso.autor.bio;
            document.getElementById("autorFoto").src = curso.autor.foto || "https://via.placeholder.com/100";
        } else {
            mensaje.textContent = "Curso no encontrado.";
        }
    } catch (err) {
        mensaje.textContent = "Error al cargar el curso.";
        console.error(err);
    }

    document.getElementById("btnInscribir").addEventListener("click", async () => {
        try {
            alert("✅ Inscripción exitosa.");

            const res = await fetch("/api/inscribir", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ usuario, curso_id: cursoId }),
            });

        } catch (err) {
            mensaje.textContent = "Error al inscribirse.";
            console.error(err);
        }
    });
});