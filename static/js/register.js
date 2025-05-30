document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formRegistro");
  const mensaje = document.getElementById("mensaje");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const usuario = document.getElementById("usuario").value;
    const correo = document.getElementById("correo").value;
    const contrasena = document.getElementById("contrasena").value;

    const checkboxes = document.querySelectorAll('input[name="intereses"]:checked');
    const intereses = Array.from(checkboxes).map(cb => cb.value);

    const datos = { usuario, correo, contrasena, intereses };

    try {
      const res = await fetch("/api/register", {
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
          window.location.href = "/login";
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
