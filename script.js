const msgInput = document.getElementById("msgInput");

// Input focus -> body scroll lock
msgInput.addEventListener("focus", () => {
  document.body.style.overflow = "hidden";
});

// Input blur -> body scroll restore
msgInput.addEventListener("blur", () => {
  document.body.style.overflow = "auto";
});
