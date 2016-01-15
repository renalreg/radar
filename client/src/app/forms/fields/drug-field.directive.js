(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmDrugField', ['store', '_', function(store, _) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/drug-field.html'
    };
  }]);
})();
