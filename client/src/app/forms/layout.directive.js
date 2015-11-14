(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmLayout', function() {
    return {
      controller: ['$attrs', function($attrs) {
        this.layout = $attrs.frmLayout;
      }]
    };
  });
})();
