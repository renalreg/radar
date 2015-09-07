(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmUnitField', function(_, session, store) {
    function sortUnits(units) {
      return _.sortBy(units, function(x) {
        return x.name.toUpperCase();
      });
    }

    return {
      require: '^frmField',
      restrict: 'A',
      scope: {
        model: '=',
        required: '='
      },
      templateUrl: 'app/fields/unit-field.html',
      link: function(scope, element, attrs, fieldCtrl) {
        scope.$watch('required', function(value) {
          fieldCtrl.setRequired(value);
        });

        var user = session.user;

        if (user.isAdmin) {
          store.findMany('units').then(function(units) {
            scope.units = sortUnits(units);
          });
        } else {
          var units = session.user.units;
          scope.units = sortUnits(units);
        }
      }
    };
  });
})();


