(function() {
  'use strict';

  var app = angular.module('radar.logs');

  function controllerFactory(
    ListController,
    $injector,
    ListHelperProxy,
    store
  ) {
    function LogListController($scope) {
      var self = this;

      $injector.invoke(ListController, self, {$scope: $scope});

      $scope.filters = {};

      var proxy = new ListHelperProxy(search, {
        perPage: 100,
        sortBy: 'date',
        reverse: true
      });
      proxy.load();

      $scope.proxy = proxy;
      $scope.search = search;
      $scope.clear = clear;
      $scope.count = 0;

      function search() {
        var proxyParams = proxy.getParams();
        var params = angular.extend({}, proxyParams, $scope.filters);

        return self.load(store.findMany('logs', params, true).then(function(data) {
          proxy.setItems(data.data);
          proxy.setCount(data.pagination.count);
          $scope.count = data.pagination.count;
          return data.data;
        }));
      }

      function clear() {
        $scope.filters = {};
        search();
      }
    }

    LogListController.$inject = ['$scope'];
    LogListController.prototype = Object.create(ListController.prototype);

    return LogListController;
  }

  controllerFactory.$inject = [
    'ListController',
    '$injector',
    'ListHelperProxy',
    'store'
  ];

  app.factory('LogListController', controllerFactory);
})();
