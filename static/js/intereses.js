document.addEventListener("DOMContentLoaded", async () => {
    const form = document.getElementById("registrar_intereses");
    const mensaje = document.getElementById("mensaje");
    const submitBtn = document.querySelector(".next_interest");
    const contador = document.getElementById("contador");
    const recomendadosBtn = document.getElementById("recomendados");
    const limpiarBtn = document.getElementById("limpiar");

    if (!form) {
        console.error("Form with ID 'registrar_intereses' not found");
        return;
    }

    submitBtn.style.display = "none";

    // Fetch categories from /api/categorias
    let intereses = [];
    try {
        const res = await fetch("/api/categorias");
        if (!res.ok) throw new Error("Failed to fetch categories");
        intereses = await res.json();
        console.log("Fetched categories:", intereses);
    } catch (err) {
        console.error("Error fetching categories:", err);
        mensaje.textContent = "Error al cargar las categorías.";
        mensaje.style.color = "red";
        return;
    }

    // Generar checkboxes dinámicamente
    const contenedor = document.getElementById("intereses");
    intereses.forEach(interes => {
        const label = document.createElement("label");
        label.className = "interes";

        const input = document.createElement("input");
        input.type = "checkbox";
        input.name = "intereses";
        input.value = interes;

        const span = document.createElement("span");
        span.textContent = interes;

        label.appendChild(input);
        label.appendChild(span);
        contenedor.appendChild(label);
    });

    // Actualizar contador de intereses seleccionados
    const actualizarContador = () => {
        const checkboxes = document.querySelectorAll('input[name="intereses"]');
        const seleccionados = Array.from(checkboxes).filter(cb => cb.checked).length;
        contador.textContent = `${seleccionados} de ${checkboxes.length} seleccionados`;
        submitBtn.style.display = seleccionados >= 3 ? "inline-block" : "none";
    };

    // Evento para checkboxes
    const checkboxes = document.querySelectorAll('input[name="intereses"]');
    checkboxes.forEach(cb => {
        cb.addEventListener("change", actualizarContador);
    });

    // Evento para seleccionar recomendados
    recomendadosBtn.addEventListener("click", () => {
        const recomendados = ["Diseño Gráfico", "Fotografía", "Programación"];
        checkboxes.forEach(cb => {
            cb.checked = recomendados.includes(cb.value);
        });
        actualizarContador();
    });

    // Evento para limpiar selección
    limpiarBtn.addEventListener("click", () => {
        checkboxes.forEach(cb => (cb.checked = false));
        actualizarContador();
    });

    // Evento de envío del formulario
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        console.log("Form submission intercepted");

        const checkboxes = document.querySelectorAll('input[name="intereses"]:checked');
        const intereses = Array.from(checkboxes).map(cb => cb.value);

        // Validar que se hayan seleccionado al menos 3 intereses
        if (intereses.length < 3) {
            mensaje.textContent = "Por favor, selecciona al menos 3 intereses.";
            mensaje.style.color = "red";
            console.log("Validation failed: Less than 3 interests selected");
            return;
        }

        const datos = { intereses };

        try {
            console.log("Sending POST to /api/intereses with data:", datos);
            const res = await fetch("/api/intereses", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(datos),
            });

            const json = await res.json();
            console.log("Response from /api/intereses:", json);

            if (res.ok) {
                mensaje.textContent = "Registro exitoso 🎉";
                mensaje.style.color = "green";
                form.reset();
                actualizarContador();
                submitBtn.style.display = "none";
                setTimeout(() => {
                    console.log("Redirecting to /feed");
                    window.location.href = "/feed";
                }, 1500);
            } else {
                mensaje.textContent = json.error || "Error al registrar.";
                mensaje.style.color = "red";
                console.error("Error response from server:", json.error);
            }
        } catch (err) {
            mensaje.textContent = "Error de conexión con el servidor.";
            mensaje.style.color = "red";
            console.error("Network or server error:", err);
        }
    });
});