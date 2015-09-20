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

      function search() {
        var proxyParams = proxy.getParams();
        var params = angular.extend({}, proxyParams, $scope.filters);

        self.load(store.findMany('users', params, true).then(function(data) {
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
