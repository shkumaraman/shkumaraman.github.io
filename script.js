 function updateOutput() {
  const code = document.getElementById('editor').value;
  const outputIframe = document.getElementById('output-iframe');
  try {
    const htmlContent = `${codeMap['html']}<style>${codeMap['css']}</style><script>${codeMap['js']}&lt;/script&gt;`;
    outputIframe.srcdoc = `<html><head></head><body>${htmlContent}</body></html>`;
    outputIframe.classList.remove('error');
  } catch (error) {
    outputIframe.srcdoc = `<span style="color: red;">${error.message}</span>`;
    outputIframe.classList.add('error');
  }
  updateLineNumbers();
  codeMap[activeTab] = code;
  saveLocalStorage();
}
