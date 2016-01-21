(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmDiagnosisField', ['store', '_', function(store, _) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/diagnosis-field.html'
    };
  }]);
})();
