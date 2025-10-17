// ===============================
// Theme Toggle Functionality
// ===============================
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Initialize theme from localStorage or system preference
function initializeTheme() {
  const savedTheme = localStorage.getItem('theme') ||
    (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  
  if (savedTheme === 'light') {
    body.classList.add('light-mode');
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
  } else {
    body.classList.remove('light-mode');
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
  }
}

// Toggle theme between light and dark
function toggleTheme() {
  body.classList.toggle('light-mode');

  if (body.classList.contains('light-mode')) {
    localStorage.setItem('theme', 'light');
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
  } else {
    localStorage.setItem('theme', 'dark');
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
  }
}

// Initialize theme on DOM load
document.addEventListener('DOMContentLoaded', initializeTheme);

// Add toggle button listener
if (themeToggle) {
  themeToggle.addEventListener('click', toggleTheme);
}

// ===============================
// Chat Layout Adjustments
// ===============================
const msgInput = document.getElementById("msgInput");
const chatLog = document.getElementById("chatLog");
const chatControls = document.querySelector(".chat-controls");
const appHeader = document.querySelector(".app-header");

// Set chatLog height based on window size
function setChatLogHeight() {
  const windowHeight = window.innerHeight;
  const headerHeight = appHeader.offsetHeight;
  const controlsHeight = chatControls.offsetHeight;

  const availableHeight = windowHeight - headerHeight - controlsHeight;
  chatLog.style.height = availableHeight + "px";
}

// Adjust chatLog height on page load
window.addEventListener("load", setChatLogHeight);

// Adjust chatLog height on window resize
window.addEventListener("resize", setChatLogHeight);

// Lock scroll when input is focused
msgInput.addEventListener("focus", () => {
  document.body.style.overflow = "hidden";
});

// Restore scroll when input loses focus
msgInput.addEventListener("blur", () => {
  document.body.style.overflow = "auto";
});
