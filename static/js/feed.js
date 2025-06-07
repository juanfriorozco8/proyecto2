document.addEventListener("DOMContentLoaded", async () => {
    const usuario = sessionStorage.getItem("usuario");
    const misCursosContainer = document.getElementById("mis-cursos");
    const recomendadosContainer = document.getElementById("recomendados");
    const usuariosSimilaresContainer = document.getElementById("usuarios-similares");
    const mensaje = document.getElementById("mensaje");
    const categoriaSelect = document.getElementById("categoria");
    const ordenSelect = document.getElementById("orden");

    if (!usuario) {
        mensaje.textContent = "No has iniciado sesión.";
        console.error("No se encontró usuario en sessionStorage");
        window.location.href = "/login";
        return;
    }
    console.log("Usuario:", usuario);

    // Cargar categorías
    try {
        const resCategorias = await fetch("/api/categorias");
        const categorias = await resCategorias.json();
        console.log("Categorías:", categorias);
        categorias.forEach(cat => {
            const option = document.createElement("option");
            option.value = cat;
            option.textContent = cat;
            categoriaSelect.appendChild(option);
        });
    } catch (err) {
        console.error("Error al cargar categorías:", err);
        mensaje.textContent = "Error al cargar categorías.";
    }

    window.cargarCursos = async () => {
        try {
            // Mostrar loading
            mensaje.textContent = "Cargando recomendaciones...";
            misCursosContainer.innerHTML = "<p>Cargando...</p>";
            recomendadosContainer.innerHTML = "<p>Cargando...</p>";
            usuariosSimilaresContainer.innerHTML = "<p>Cargando...</p>";

            console.log("Enviando petición con:", {
                usuario,
                categoria: categoriaSelect.value,
                orden: ordenSelect.value
            });

            const res = await fetch("/api/feed", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({
                    usuario,
                    categoria: categoriaSelect.value || "",
                    orden: ordenSelect.value || "compatibilidad"
                }),
            });

            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            const data = await res.json();
            console.log("Datos recibidos del backend:", data);

            // Limpiar containers
            misCursosContainer.innerHTML = "";
            recomendadosContainer.innerHTML = "";
            usuariosSimilaresContainer.innerHTML = "";
            mensaje.textContent = "";

            // Validar estructura de datos
            if (!data || typeof data !== 'object') {
                throw new Error("Respuesta inválida del servidor");
            }

            // Mis cursos
            if (data.mis_cursos && Array.isArray(data.mis_cursos) && data.mis_cursos.length > 0) {
                console.log(`Mostrando ${data.mis_cursos.length} cursos inscritos`);
                data.mis_cursos.forEach((curso, index) => {
                    try {
                        const div = document.createElement("div");
                        div.className = "card";
                        div.innerHTML = `
                            <img src="${curso.foto || 'https://via.placeholder.com/150'}" alt="${curso.titulo || 'Sin título'}" />
                            <h3>${curso.titulo || 'Sin título'}</h3>
                            <p><strong>Categoría:</strong> ${curso.categoria || 'Sin categoría'}</p>
                            <p><strong>Dificultad:</strong> ${curso.dificultad || 'No especificada'}</p>
                            <p><strong>Duración:</strong> ${curso.duracion || 'No especificada'}</p>
                            <p><strong>Rating:</strong> ${curso.rating || 0}/5</p>
                            <p><strong>Compatibilidad:</strong> ${curso.compatibilidad || 0}%</p>
                            <p><strong>Estado:</strong> <span class="inscrito">Inscrito</span></p>
                            <button class="next" onclick="verCurso('${curso.id}')">Ver más</button>
                        `;
                        misCursosContainer.appendChild(div);
                    } catch (err) {
                        console.error(`Error al renderizar curso inscrito ${index}:`, err, curso);
                    }
                });
            } else {
                misCursosContainer.innerHTML = "<p>No tienes cursos inscritos.</p>";
            }

            // Cursos recomendados
            if (data.recomendados && Array.isArray(data.recomendados) && data.recomendados.length > 0) {
                console.log(`Mostrando ${data.recomendados.length} cursos recomendados`);
                
                // Header con contador
                const headerDiv = document.createElement("div");
                headerDiv.className = "recomendados-header";
                headerDiv.innerHTML = `<p><strong>${data.recomendados.length} cursos recomendados para ti</strong></p>`;
                recomendadosContainer.appendChild(headerDiv);

                data.recomendados.forEach((curso, index) => {
                    try {
                        const div = document.createElement("div");
                        div.className = "card recomendado";
                        
                        // Validar que siempre tenga razones
                        const tieneRazones = curso.razones && Array.isArray(curso.razones) && curso.razones.length > 0;
                        if (!tieneRazones) {
                            console.warn(`Curso sin razones detectado:`, curso);
                        }

                        div.innerHTML = `
                            <img src="${curso.foto || 'https://via.placeholder.com/150'}" alt="${curso.titulo || 'Sin título'}" />
                            <h3>${curso.titulo || 'Sin título'}</h3>
                            <p><strong>Categoría:</strong> ${curso.categoria || 'Sin categoría'}</p>
                            <p><strong>Dificultad:</strong> ${curso.dificultad || 'No especificada'}</p>
                            <p><strong>Duración:</strong> ${curso.duracion || 'No especificada'}</p>
                            <p><strong>Rating:</strong> ${curso.rating || 0}/5</p>
                            <p><strong>Compatibilidad:</strong> <span class="compatibilidad-${getCompatibilidadClass(curso.compatibilidad)}">${curso.compatibilidad || 0}%</span></p>
                            ${tieneRazones ? 
                                `<div class="razones">
                                    <strong>¿Por qué te lo recomendamos?</strong>
                                    <ul>
                                        ${curso.razones.map(razon => `<li>${razon}</li>`).join('')}
                                    </ul>
                                </div>` : 
                                '<p class="sin-razones">Sin razones específicas</p>'
                            }
                            <button class="next" onclick="verCurso('${curso.id}')">Ver más</button>
                        `;
                        recomendadosContainer.appendChild(div);
                    } catch (err) {
                        console.error(`Error al renderizar curso recomendado ${index}:`, err, curso);
                    }
                });
            } else {
                recomendadosContainer.innerHTML = "<p>No hay cursos recomendados en este momento. Intenta ajustar los filtros o actualiza tus intereses.</p>";
            }

            // Usuarios similares
            if (data.usuarios_similares && Array.isArray(data.usuarios_similares) && data.usuarios_similares.length > 0) {
                console.log(`Mostrando ${data.usuarios_similares.length} usuarios similares`);
                data.usuarios_similares.forEach((u, index) => {
                    try {
                        const div = document.createElement("div");
                        div.className = "card usuario-similar";
                        div.innerHTML = `
                            <div class="usuario-avatar">👤</div>
                            <h3>${u.usuario || 'Usuario anónimo'}</h3>
                            <p><strong>Similitud:</strong> <span class="similitud-${getSimilitudClass(u.similitud)}">${u.similitud || 0}%</span></p>
                            <button class="next" onclick="verPerfilUsuario('${u.usuario}')">Ver perfil</button>
                        `;
                        usuariosSimilaresContainer.appendChild(div);
                    } catch (err) {
                        console.error(`Error al renderizar usuario similar ${index}:`, err, u);
                    }
                });
            } else {
                usuariosSimilaresContainer.innerHTML = "<p>No hay usuarios similares en este momento.</p>";
            }

            // Mensaje de éxito
            console.log("✅ Feed cargado exitosamente");

        } catch (err) {
            console.error("❌ Error en cargarCursos:", err);
            mensaje.textContent = `Error al cargar los datos: ${err.message}`;
            
            // Mostrar mensaje de error en containers
            misCursosContainer.innerHTML = "<p>Error al cargar cursos inscritos.</p>";
            recomendadosContainer.innerHTML = "<p>Error al cargar recomendaciones.</p>";
            usuariosSimilaresContainer.innerHTML = "<p>Error al cargar usuarios similares.</p>";
        }
    };

    // Función auxiliar para clasificar compatibilidad
    window.getCompatibilidadClass = (compatibilidad) => {
        if (compatibilidad >= 80) return 'alta';
        if (compatibilidad >= 50) return 'media';
        return 'baja';
    };

    // Función auxiliar para clasificar similitud
    window.getSimilitudClass = (similitud) => {
        if (similitud >= 70) return 'alta';
        if (similitud >= 40) return 'media';
        return 'baja';
    };

    // Event listeners para filtros
    categoriaSelect.addEventListener('change', () => {
        console.log("Categoría cambiada a:", categoriaSelect.value);
        cargarCursos();
    });

    ordenSelect.addEventListener('change', () => {
        console.log("Orden cambiado a:", ordenSelect.value);
        cargarCursos();
    });

    // Cargar datos iniciales
    console.log("🚀 Iniciando carga inicial del feed");
    await cargarCursos();
});

// Funciones globales
function verCurso(id) {
    if (!id) {
        console.error("ID de curso no válido:", id);
        return;
    }
    console.log("Navegando a curso:", id);
    sessionStorage.setItem("curso_id", id);
    window.location.href = `/curso?id=${id}`;
}

function verPerfilUsuario(usuario) {
    if (!usuario) {
        console.error("Usuario no válido:", usuario);
        return;
    }
    console.log("Navegando a perfil de usuario:", usuario);
    sessionStorage.setItem("perfil_usuario", usuario);
    window.location.href = `/perfil_usuario?usuario=${usuario}`;
}

// Función para refrescar el feed manualmente
window.refrescarFeed = async () => {
    console.log("🔄 Refrescando feed manualmente");
    await cargarCursos();
};

// Debug: Función para inspeccionar datos
window.debugFeed = () => {
    console.log("=== DEBUG FEED ===");
    console.log("Usuario actual:", sessionStorage.getItem("usuario"));
    console.log("Categoría seleccionada:", document.getElementById("categoria").value);
    console.log("Orden seleccionado:", document.getElementById("orden").value);
};