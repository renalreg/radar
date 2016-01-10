(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmObservationField', ['store', '_', function(store, _) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/observation-field.html',
      link: function(scope) {
        store.findMany('observations').then(function(observations) {
          scope.observations = _.sortBy(observations, 'name');
        });
      }
    };
  }]);
})();
