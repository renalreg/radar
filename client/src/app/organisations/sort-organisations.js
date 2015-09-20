(function() {
  'use strict';

  var app = angular.module('radar.organisations');

  app.factory('sortOrganisations', ['_', function(_) {
    function sortByName(x) {
      return x.name.toUpperCase();
    }

    function sortByType(x) {
      // Other organisations first (NHS etc.)
      return x.type === 'OTHER' ? 0 : 1;
    }

    return function sortOrganisations(organisations) {
      return _.sortByAll(organisations, sortByType, sortByName);
    };
  }]);
})();
