(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmConsentField', function() {
    return {
      restrict: 'A',
      scope: {
        model: '='
      },
      transclude: true,
      templateUrl: 'app/forms/fields/consent-field.html'
    };
  });
})();
