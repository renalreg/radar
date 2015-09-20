(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmOrganisationField', ['sortOrganisations', 'store', function(sortOrganisations, store) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/organisation-field.html',
      link: function(scope) {
        store.findMany('organisations').then(function(organisations) {
          scope.organisations = sortOrganisations(organisations);
        });
      }
    };
  }]);
})();
