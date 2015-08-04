(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrDialysisEditor', function() {
    return {
      restrict: 'A',
      scope: {
        patient: '='
      },
      templateUrl: 'app/dialysis/dialysis-editor.html',
      controller: 'DialysisEditorController'
    };
  });
})();
