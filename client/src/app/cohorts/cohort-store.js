(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  app.factory('cohortStore', ['store', '$q', function(store, $q) {
    return {
      findOne: function(id) {
        return store.findOne('groups', id, true).then(function(group) {
          if (group.type === 'COHORT') {
            return group;
          } else {
            $q.reject();
          }
        });
      },
      findMany: function() {
        return store.findMany('groups', {type: 'COHORT'});
      }
    };
  }]);
})();
