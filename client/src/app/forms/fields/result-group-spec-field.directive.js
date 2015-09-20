(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmResultGroupSpecField', ['store', '_', function(store, _) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/result-group-spec-field.html',
      link: function(scope) {
        store.findMany('result-group-specs').then(function(resultGroupSpecs) {
          scope.resultGroupSpecs = _.sortBy(resultGroupSpecs, 'name');
        });
      }
    };
  }]);
})();
