document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registrar_intereses");
  const mensaje = document.getElementById("mensaje");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const checkboxes = document.querySelectorAll('input[name="intereses"]:checked');
    const intereses = Array.from(checkboxes).map(cb => cb.value);

    const datos = { intereses };

    try {
      const res = await fetch("/api/intereses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
      });

      const json = await res.json();

      if (res.ok) {
        mensaje.textContent = "Registro exitoso 🎉";
        mensaje.style.color = "green";
        form.reset();
        setTimeout(() => {
          window.location.href = "/feed";
        }, 1500);
      } else {
        mensaje.textContent = json.error || "Error al registrar.";
        mensaje.style.color = "red";
      }
    } catch (err) {
      mensaje.textContent = "Error de conexión con el servidor.";
      mensaje.style.color = "red";
      console.error(err);
    }
  });
});

const intereses = [
  "Diseño Gráfico", "Ilustración", "Fotografía",
  "Animación", "Escritura creativa", "Música",
  "Programación", "Dibujo", "Escultura",
  "Tejer", "Joyería", "Cocina"
];

const contenedor = document.getElementById("intereses");

intereses.forEach(interes => {
  const label = document.createElement("label");
  label.className = "intereses_box";

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
