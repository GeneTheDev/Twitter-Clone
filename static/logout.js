document.addEventListener("DOMContentLoaded", () => {
  const logout = document.querySelector(".nav-link.logout");

  if (logout) {
    logout.addEventListener("click", (event) => {
      event.preventDefault();

      fetch("/logout", { method: "POST" })
        .then((response) => {
          window.location.href = "/login";
        })
        .catch((error) => {
          console.error(error);
        });
    });
  }
});
