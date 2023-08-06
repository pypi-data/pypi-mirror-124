(function (factory) {
  if (typeof define === 'function' && define.amd) {
    require(['jquery', 'iframeResizer'], factory);
  } else {
    factory(window.jQuery, window.iFrameResize);
  }
}(function ($, iFrameResize) {
  "use strict";
  var default_options = {
    inPageLinks: true,
  }

  function initIFrame() {
      var iframe = $(this);

      if (iframe.data('autoSize') === 'True') {
        var set_options = iframe.data('resizerOptions');

        var autoJump = { onResized: function () {scroll(0, 0);} };
        if (iframe.data('autoJump') !== 'True') {
          autoJump = {}
        }

        var options = $.extend({},default_options,set_options, autoJump);
        iFrameResize(options, this);
      }

      iframe.prev().removeClass('loading');
  }

  // We have to wait for the ready and then add the onload event listener directly on the
  // iframe because the iframe does not propagate the onload back to document.
  $(document).ready(function () {
    $('iframe').on('load', initIFrame);

    $(document).on('onBeforeClose', '.overlay', function () {
      $('iframe').each(initIFrame);
    });
  });
}));
