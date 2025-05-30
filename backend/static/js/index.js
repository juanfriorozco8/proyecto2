document.addEventListener("DOMContentLoaded", () => {
  const usuario = localStorage.getItem("usuario");

  if (usuario) {
    // Si ya hay usuario en sesión, redirige al feed automáticamente
    window.location.href = "feed";
  } else {
    // Si no hay usuario, activa los botones para navegar a login y registro
    const btnLogin = document.getElementById("btnLogin");
    const btnRegister = document.getElementById("btnRegister");

    if (btnLogin) {
      btnLogin.addEventListener("click", () => {
        //console.log(window.location.href)
        window.location.href = "login";
      });
    }

    if (btnRegister) {
      btnRegister.addEventListener("click", () => {
        window.location.href = "register";
      });
    }
  }
});
