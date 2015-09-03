(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmHelp', function() {
    return {
      templateUrl: 'app/forms/help.html',
      transclude: true
    };
  });
})();
