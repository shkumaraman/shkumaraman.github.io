const msgInput = document.getElementById("msgInput");
const chatLog = document.getElementById("chatLog");
const chatControls = document.querySelector(".chat-controls");
const appHeader = document.querySelector(".app-header");

// Function to set chatLog height
function setChatLogHeight() {
  const windowHeight = window.innerHeight;
  const headerHeight = appHeader.offsetHeight;
  const controlsHeight = chatControls.offsetHeight;
  
  const availableHeight = windowHeight - headerHeight - controlsHeight;
  chatLog.style.height = availableHeight + "px";
}

// On page load
setChatLogHeight();

// On window resize
window.addEventListener("resize", setChatLogHeight);

// Input focus -> body scroll lock
msgInput.addEventListener("focus", () => {
  document.body.style.overflow = "hidden";
});

// Input blur -> body scroll restore
msgInput.addEventListener("blur", () => {
  document.body.style.overflow = "auto";
});
