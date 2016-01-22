(function() {
  'use strict';

  var app = angular.module('radar.groups');

  app.factory('sortGroups', ['_', function(_) {
    // TODO sort by type first
    return function sortGroups(groups) {
      return _.sortBy(groups, function(x) {
        return x.name.toUpperCase();
      });
    };
  }]);
})();
