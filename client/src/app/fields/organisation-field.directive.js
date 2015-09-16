(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmOrganisationField', function(_, store) {
    function sortByName(x) {
      return x.name.toUpperCase();
    }

    function sortByType(x) {
      // Other organisations first (NHS etc.)
      return x.type === 'OTHER' ? 0 : 1;
    }

    function sortOrganisations(organisations) {
      return _.sortByAll(organisations, sortByType, sortByName);
    }

    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/fields/organisation-field.html',
      link: function(scope) {
        store.findMany('organisations').then(function(organisations) {
          scope.organisations = sortOrganisations(organisations);
        });
      }
    };
  });
})();
