document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".primary-button");

  if (!button) {
    return;
  }

  button.addEventListener("click", () => {
    button.classList.add("is-visited");
    window.setTimeout(() => button.classList.remove("is-visited"), 350);
  });
});