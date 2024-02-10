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
          <script>${jsCode}</script>
        </head>
        <body>${htmlCode}</body>
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
