// ----------------- Theme Toggle -----------------
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Load theme from localStorage or system preference
const savedTheme = localStorage.getItem('theme') ||
                   (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');

if (savedTheme === 'light') {
  body.classList.add('light-mode');
  themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
} else {
  themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
}

themeToggle.addEventListener('click', () => {
  body.classList.toggle('light-mode');
  if (body.classList.contains('light-mode')) {
    localStorage.setItem('theme', 'light');
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
  } else {
    localStorage.setItem('theme', 'dark');
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
  }
});
