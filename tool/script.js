const combinedCode = `
  <html>
    <head>
      <style>${codeMap['css']}</style>
    </head>
    <body>
      ${codeMap['html']}
      <script>
        ${codeMap['js']}
        runScript();
      </script>
    </body>
  </html>
`;

const blob = new Blob([combinedCode], { type: 'text/html' });
const url = URL.createObjectURL(blob);
outputIframe.src = url;
