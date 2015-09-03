(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmLayout', function(_) {
    return {
      controller: function($attrs) {
        this.layout = $attrs.frmLayout;
      }
    };
  });
})();

