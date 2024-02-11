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

  const doc = outputIframe.contentDocument;
  doc.open();
  doc.write(combinedCode);
  doc.close();
}
