(function() {
  'use strict';

  var app = angular.module('radar.hospitals');

  app.factory('hospitalStore', ['store', '$q', function(store, $q) {
    return {
      findOne: function(id) {
        return store.findOne('groups', id, true).then(function(group) {
          if (group.type === 'HOSPITAL') {
            return group;
          } else {
            $q.reject();
          }
        });
      },
      findMany: function(params) {
        if (params === undefined) {
          params = {};
        }

        params.type = 'HOSPITAL';

        return store.findMany('groups', params);
      }
    };
  }]);
})();
