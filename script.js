let activeTab = 'html';
    let codeMap = {
      'html': '',
      'css': '',
      'js': '',
      'txt': ''
    };

  let darkMode = localStorage.getItem('darkMode') === 'true' || false;

    window.onload = function () {
      loadLocalStorage();
      loadActiveTab();
      loadCode();
      updateButtonColor();
      applyDarkModeStyles();
    };

function changeTab(tab) {
  if (activeTab !== tab) {
    activeTab = tab;
    loadCode();
    updateActiveTabStyle();
    updateButtonColor();
    
    localStorage.setItem('activeTab', activeTab); // Store the active tab in local storage
  }
}

function loadActiveTab() {
  const storedActiveTab = localStorage.getItem('activeTab');
  if (storedActiveTab && storedActiveTab !== activeTab) {
    activeTab = storedActiveTab;
    changeTab(activeTab);
  }
}
  
    function updateButtonColor() {
      const tabs = document.querySelectorAll('.tab');
      tabs.forEach(tab => {
        const lang = tab.getAttribute('onclick').match(/\('(.*?)'\)/)[1];
        if (lang === activeTab) {
          tab.classList.add('active-tab');
        } else {
          tab.classList.remove('active-tab');
        }
      });
    }

  function downloadCode() {
  let codeToDownload = codeMap[activeTab];

  const blob = new Blob([codeToDownload], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `code_${activeTab}.txt`;
  link.click();
}

function copyCode() {
  let codeToCopy = codeMap[activeTab];

  navigator.clipboard.writeText(codeToCopy)
    .then(() => alert('Code copied to clipboard'))
    .catch(error => console.error('Unable to copy code', error));
}

function deleteCode() {
  codeMap[activeTab] = '';
  document.getElementById('editor').value = '';
  updateOutput();
  updateLineNumbers(); 
}

    function updateLineNumbers() {
      const editor = document.getElementById('editor');
      const lineNumbers = document.getElementById('line-numbers');

      let lines = editor.value.split('\n');
      let numbers = '';

      for (let i = 1; i <= lines.length; i++) {
        numbers += i + '<br>';
      }

      lineNumbers.innerHTML = numbers;
    }

    function syncScroll() {
      const lineNumbers = document.getElementById('line-numbers');
      const editor = document.getElementById('editor');

      lineNumbers.scrollTop = editor.scrollTop;
    }

    function loadCode() {
      document.getElementById('editor').value = codeMap[activeTab];
      updateOutput();
    }

    function updateActiveTabStyle() {
      const tabs = document.querySelectorAll('.tab');
      tabs.forEach(tab => tab.classList.remove('active-tab'));

      const activeTabElement = document.querySelector(`.tab[data-lang="${activeTab}"]`);
      if (activeTabElement) {
        activeTabElement.classList.add('active-tab');
      }
    }

    function toggleFullScreen() {
      const elem = document.documentElement;
      if (!document.fullscreenElement) {
        elem.requestFullscreen().catch(err => {
          console.log(`Error attempting to enable full-screen mode: ${err.message}`);
        });
      } else {
        document.exitFullscreen();
      }
    }

function toggleDarkMode() {
  darkMode = !darkMode;
  applyDarkModeStyles();
  localStorage.setItem('darkMode', darkMode);
  }
  
function applyDarkModeStyles() {
  const body = document.body;
  const editor = document.getElementById('editor');
  const outputContainer = document.getElementById('output-container');
  const lineNumbers = document.getElementById('line-numbers');
  const snippetButtons = document.querySelectorAll('#left-menu .btn1');

  if (darkMode) {
    body.style.backgroundColor = '#000';
    body.style.color = '#fff';
    editor.style.backgroundColor = '#000';
    lineNumbers.style.color = '#fff';

    // Update snippet buttons in dark mode
    snippetButtons.forEach(button => {
      button.style.backgroundColor = '#000';
      button.style.color = '#fff';
    });

    document.getElementById('dark-mode-btn').innerHTML = '<i class="fas fa-sun"></i>';
  } else {
    body.style.backgroundColor = '#fff';
    body.style.color = '#000';
    editor.style.backgroundColor = '#fff';
    lineNumbers.style.color = '#000';

    // Update snippet buttons in light mode
    snippetButtons.forEach(button => {
      button.style.backgroundColor = '#fff';
      button.style.color = '#000';
    });

    document.getElementById('dark-mode-btn').innerHTML = '<i class="fas fa-moon"></i>';
  }
  updateEditorTextColor();
  }

    function updateEditorTextColor() {
      const editor = document.getElementById('editor');
      editor.style.color = darkMode ? '#fff' : '#000';
    }

    function saveLocalStorage() {
      localStorage.setItem('codeMap', JSON.stringify(codeMap));
    }

    function loadLocalStorage() {
      const savedCodeMap = localStorage.getItem('codeMap');

      if (savedCodeMap) {
        codeMap = JSON.parse(savedCodeMap);
        loadCode();
      }
    }

    function importCode() {
      const importLink = prompt("Enter the import raw link:");
      if (importLink) {
        fetch(importLink)
          .then(response => response.text())
          .then(data => {
            codeMap[activeTab] = data;
            loadCode();
            updateOutput();
          })
          .catch(error => console.error('Error importing code', error));
      }
    }

    // New function for inserting snippets at the cursor position
    function insertSnippet(snippet) {
      const editor = document.getElementById('editor');
      const start = editor.selectionStart;
      const end = editor.selectionEnd;

      // Insert the snippet at the cursor position
      editor.value = editor.value.substring(0, start) + snippet + editor.value.substring(end);
      
      // Move the cursor to the end of the inserted snippet
      editor.selectionStart = editor.selectionEnd = start + snippet.length;

      // Trigger the input event to update the output
      editor.dispatchEvent(new Event('input', { bubbles: true }));
    }
  
  function undo() {
  const editor = document.getElementById('editor');
  const undoActionSuccess = document.execCommand('undo');

  if (undoActionSuccess) {
    codeMap[activeTab] = editor.value;
    updateOutput();
    updateLineNumbers();
  }
  }

function updateOutput() {
  const htmlCode = codeMap['html'];
  const cssCode = codeMap['css'];
  const jsCode = codeMap['js'];
  const outputIframe = document.getElementById('output-iframe');

  try {
    const htmlContent = `
      <html>
        <head>
          <style>${cssCode}</style>
        </head>
        <body>
          ${htmlCode}
          <script>${jsCode}</script>
        </body>
      </html>`;
    outputIframe.srcdoc = htmlContent;
    outputIframe.classList.remove('error');
  } catch (error) {
    outputIframe.srcdoc = `<span style="color: red;">${error.message}</span>`;
    outputIframe.classList.add('error');
  }

  updateLineNumbers();
  codeMap[activeTab] = document.getElementById('editor').value;
  saveLocalStorage();
}
