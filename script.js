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
      let codeToDownload = codeMap['html'] + '\n' + codeMap['css'] + '\n' + codeMap['js'] + '\n' + codeMap['txt'];

      const blob = new Blob([codeToDownload], { type: 'text/plain' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'code.txt';
      link.click();
    }

    function copyCode() {
      let codeToCopy = codeMap['html'] + '\n' + codeMap['css'] + '\n' + codeMap['js'] + '\n' + codeMap['txt'];

      navigator.clipboard.writeText(codeToCopy)
        .then(() => alert('Code copied to clipboard'))
        .catch(error => console.error('Unable to copy code', error));
    }

    function deleteCode() {
      document.getElementById('editor').value = '';
      updateOutput();
      updateLineNumbers();
    }

function updateOutput() {
  const outputIframe = document.getElementById('output-iframe');
  const htmlCode = codeMap['html'];
  const cssCode = codeMap['css'];
  const jsCode = codeMap['js'];

  const combinedCode = `
    <html lang="en">
    <head>
      <style>${cssCode}</style>
    </head>
    <body>
      ${htmlCode}
      <script>${jsCode}</script>
    </body>
    </html>
  `;

  try {
    const doc = outputIframe.contentDocument;
    doc.open();
    doc.write(combinedCode);
    doc.close();
  } catch (error) {
    console.error('Error updating output:', error);
  }
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
  const searchBox = document.getElementById('search-box');
  const searchButtons = document.querySelectorAll('#search-box button');
  
  if (darkMode) {
    body.style.backgroundColor = '#333';
    body.style.color = '#fff';
    editor.style.backgroundColor = '#333';
    lineNumbers.style.color = '#fff';
    searchBox.style.backgroundColor = '#333';
    
    // Update snippet buttons in dark mode
    snippetButtons.forEach(button => {
      button.style.backgroundColor = '#333';
      button.style.color = '#fff';
    });
    searchButtons.forEach(button => {
          button.style.backgroundColor = '#333';
          button.style.color = '#fff';
        });

    document.getElementById('dark-mode-btn').innerHTML = '<i class="fas fa-sun"></i>';
  } else {
    body.style.backgroundColor = '#fff';
    body.style.color = '#000';
    editor.style.backgroundColor = '#fff';
    lineNumbers.style.color = '#000';
    searchBox.style.backgroundColor = '#fff';
    
    // Update snippet buttons in light mode
    snippetButtons.forEach(button => {
      button.style.backgroundColor = '#fff';
      button.style.color = '#000';
    });
    searchButtons.forEach(button => {
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
  document.execCommand('undo');
  updateOutput();
  updateLineNumbers();
  }

  let currentSearchIndex = 0;

function findTextDown() {
  const editor = document.getElementById('editor');
  const searchInput = document.getElementById('search-input');
  const searchText = searchInput.value.trim();

  if (searchText === '') {
    return;
  }

  const editorContent = editor.value;
  const searchRegex = new RegExp(searchText, 'gi');

  // Find all occurrences of the search text
  const matches = [...editorContent.matchAll(searchRegex)];

  if (matches.length > 0) {
    const match = matches[currentSearchIndex % matches.length];
    const startPos = match.index;
    const endPos = startPos + searchText.length;

    editor.setSelectionRange(startPos, endPos);
    editor.focus();

    // Move to the next occurrence
    currentSearchIndex++;
  } else {
    // If no occurrences are found, reset the index
    currentSearchIndex = 0;
  }
  }
  
