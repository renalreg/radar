(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmUnitField', function(_, session, store) {
    function sortUnits(units) {
      return _.sortBy(units, function(x) {
        return x.name.toUpperCase();
      });
    }

    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/unit-field.html',
      link: function(scope) {
        var user = session.user;

        if (user.isAdmin) {
          // TODO filter
          store.findMany('organisations', {type: 'UNIT'}).then(function(units) {
            scope.units = sortUnits(units);
          });
        } else {
          // TODO filter
          scope.units = sortUnits(_.map(session.user.organisations, function(x) {
            return x.organisation;
          }));
        }
      }
    };
  });
})();
