document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const mensaje = document.getElementById("mensaje");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const usuario = document.getElementById("usuario").value;
    const contrasena = document.getElementById("contrasena").value;

    const datos = { usuario, contrasena };

    try {
      const res = await fetch("http://localhost:5050/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
      });

      const json = await res.json();

      if (res.ok) {
        localStorage.setItem("usuario", usuario);
        window.location.href = "index.html"; // Redirige al feed
      } else {
        mensaje.textContent = json.error || "Credenciales incorrectas.";
        mensaje.style.color = "red";
      }
    } catch (error) {
      console.error(error);
      mensaje.textContent = "Error de conexión con el servidor.";
      mensaje.style.color = "red";
    }
  });
});
