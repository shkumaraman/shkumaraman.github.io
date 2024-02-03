javascript:(function() {
  var adSelectors = [
    '.ads',
    '.ad-container',
    '.ad-unit',
    '.sponsored',
    '.advertisement',
    'ins.adsbygoogle',
    'iframe[src*="doubleclick.net"]',
    'iframe[src*="googlesyndication.com"]'
  ];

  adSelectors.forEach(function(selector) {
    var elements = document.querySelectorAll(selector);
    elements.forEach(function(element) {
      element.style.display = 'none';
    });
  });
})();
