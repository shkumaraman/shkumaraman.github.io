$(document).ready(function () {

  // Publish output from HTML, CSS, and JS textareas in the iframe below
  onload = (document).onkeyup = function () {
    (document.getElementById("output-iframe").contentWindow.document).write(
      html.value + "<style>" + css.value + "</style><script>" + js.value + "</script>"
    );
    (document.getElementById("output-iframe").contentWindow.document).close();
  };

});
