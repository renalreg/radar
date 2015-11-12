(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('passwordStrengthMeter', function() {
    return {
      restrict: 'A',
      scope: {
        score: '=',
      },
      template: '<div class="password-strength-meter" ng-class="\'score-\' + score"></div>'
    };
  });
})();
