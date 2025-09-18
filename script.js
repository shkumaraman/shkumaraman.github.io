const chatLog = document.getElementById("chatLog");
const msgInput = document.getElementById("msgInput");

function resizeChatLog() {
  const vh = window.innerHeight; // current viewport height
  const headerHeight = document.querySelector(".app-header").offsetHeight;
  const chatControlsHeight = document.querySelector(".chat-controls").offsetHeight;
  const typingHeight = document.getElementById("typingIndicator").offsetHeight;

  const availableHeight = vh - headerHeight - typingHeight - chatControlsHeight;
  chatLog.style.height = availableHeight + "px";
}

// Initial resize
resizeChatLog();

// Resize on window resize (keyboard open/close triggers resize)
window.addEventListener("resize", resizeChatLog);

// Optional: input focus -> body scroll lock (jaise pehle)
msgInput.addEventListener("focus", () => {
  document.body.style.overflow = "hidden";
});

msgInput.addEventListener("blur", () => {
  document.body.style.overflow = "auto";
});
