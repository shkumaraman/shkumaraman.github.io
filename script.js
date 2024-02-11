function updateOutput() {
  const htmlTextarea = codeMap['html'];
  const cssTextarea = codeMap['css'];
  const jsTextarea = codeMap['js'];

  const outputIframe = document.getElementById('output-iframe');
  const outputDocument = outputIframe.contentWindow.document;

  outputDocument.open();
  outputDocument.write(
    htmlTextarea + "<style>" + cssTextarea + "</style><script>" + jsTextarea + "</script>"
  );
  outputDocument.close();

  updateLineNumbers();
  saveLocalStorage();
}
