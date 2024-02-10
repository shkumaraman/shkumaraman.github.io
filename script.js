function updateOutput() {
  const htmlCode = codeMap['html'];
  const cssCode = codeMap['css'];
  const jsCode = codeMap['js'];
  const outputIframe = document.getElementById('output-iframe');

  try {
    const htmlContent = `${htmlCode}<style>${cssCode}</style><script>${jsCode}</script>`;
    outputIframe.srcdoc = `<html><head></head><body>${htmlContent}</body></html>`;
    outputIframe.classList.remove('error');
  } catch (error) {
    outputIframe.srcdoc = `<span style="color: red;">${error.message}</span>`;
    outputIframe.classList.add('error');
  }

  updateLineNumbers();
  saveLocalStorage();
}
