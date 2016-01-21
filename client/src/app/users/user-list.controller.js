(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('UserListController', ['ListController', '$injector', 'ListHelperProxy', 'store', function(ListController, $injector, ListHelperProxy, store) {
    function UserListController($scope) {
      var self = this;

      $injector.invoke(ListController, self, {$scope: $scope});

      var defaultFilters = {};
      $scope.filters = angular.copy(defaultFilters);

      var proxy = new ListHelperProxy(search, {perPage: 50});
      proxy.load();

      $scope.proxy = proxy;
      $scope.search = search;
      $scope.clear = clear;
      $scope.count = 0;

      function filtersToParams(filters) {
        var params = {};

        var keys = ['username', 'email', 'firstName', 'lastName'];

        _.forEach(keys, function(key) {
          var value = filters[key];

          if (value !== undefined && value !== null && value !== '') {
            params[key] = value;
          }
        });

        var groups = _.filter([filters.cohort, filters.hospital], function(group) {
          return group !== undefined && group !== null;
        });

        var groupIds = _.map(groups, function(group) {
          return group.id;
        });

        if (groupIds.length > 0) {
          params.group = groupIds.join(',');
        }

        return params;
      }

      function search() {
        var proxyParams = proxy.getParams();
        var params = angular.extend({}, proxyParams, filtersToParams($scope.filters));

        return self.load(store.findMany('users', params, true).then(function(data) {
          proxy.setItems(data.data);
          proxy.setCount(data.pagination.count);
          $scope.count = data.pagination.count;
          return data.data;
        }));
      }

      function clear() {
        $scope.filters = angular.copy(defaultFilters);
        search();
      }
    }

    UserListController.$inject = ['$scope'];
    UserListController.prototype = Object.create(ListController.prototype);

    return UserListController;
  }]);
})();
