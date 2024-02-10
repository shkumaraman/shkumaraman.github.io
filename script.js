function updateOutput() {
  const htmlCode = codeMap['html'];
  const cssCode = codeMap['css'];
  const jsCode = codeMap['js'];
  const outputIframe = document.getElementById('output-iframe');

  try {
    const htmlContent = `${htmlCode}<style>${cssCode}</style><script>${jsCode}</script>`;
    outputIframe.srcdoc = `<html><head>${cssCode}</head><body>${htmlContent}<script>${jsCode}</script></body></html>`;
    outputIframe.classList.remove('error');
  } catch (error) {
    outputIframe.srcdoc = `<span style="color: red;">${error.message}</span>`;
    outputIframe.classList.add('error');
  }

  updateLineNumbers();
  codeMap[activeTab] = document.getElementById('editor').value;
  saveLocalStorage();
}
