(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmUnitField', ['_', 'session', 'store', 'sortOrganisations', function(_, session, store, sortOrganisations) {
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
            scope.units = sortOrganisations(units);
          });
        } else {
          // TODO filter
          scope.units = sortOrganisations(_.map(session.user.organisations, function(x) {
            return x.organisation;
          }));
        }
      }
    };
  }]);
})();
