const chatLog = document.getElementById("chatLog");
const msgInput = document.getElementById("msgInput");

// Resize chat log based on available viewport height
function resizeChatLog() {
  const vh = window.innerHeight; // current viewport height
  const headerHeight = document.querySelector(".app-header").offsetHeight;
  const chatControlsHeight = document.querySelector(".chat-controls").offsetHeight;
  const typingHeight = document.getElementById("typingIndicator").offsetHeight;

  const availableHeight = vh - headerHeight - typingHeight - chatControlsHeight;

  // Set max-height so chat log shrinks on keyboard open but never smaller than min-height
  chatLog.style.maxHeight = availableHeight + "px";
}

// Initial resize
resizeChatLog();

// Resize on window resize (keyboard open/close triggers this)
window.addEventListener("resize", resizeChatLog);

// Input focus -> lock body scroll
msgInput.addEventListener("focus", () => {
  document.body.style.overflow = "hidden";
  resizeChatLog(); // ensure chat log height adjusts for keyboard
});

// Input blur -> restore body scroll
msgInput.addEventListener("blur", () => {
  document.body.style.overflow = "auto";
  resizeChatLog(); // reset chat log height
});
