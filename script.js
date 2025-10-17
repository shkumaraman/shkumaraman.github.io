// Theme toggle functionality
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
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
  }
}

// Toggle theme function
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

// Layout management
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

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize theme
  initializeTheme();
  
  // Set initial chat log height
  setChatLogHeight();
  
  // Add event listeners
  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }
  
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
});
