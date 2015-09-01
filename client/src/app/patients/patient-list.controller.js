(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientListController', function(ListController, $injector, ListHelperProxy) {
    function PatientListController($scope, store) {
      var self = this;

      $injector.invoke(ListController, self, {$scope: $scope});

      $scope.filters = {};

      var proxy = new ListHelperProxy(search, {perPage: 50});
      proxy.load();

      $scope.proxy = proxy;
      $scope.search = search;
      $scope.clear = clear;

      function search() {
        var proxyParams = proxy.getParams();
        var params = angular.extend({}, proxyParams, $scope.filters);

        self.load(store.findMany('patients', params, true).then(function(data) {
          proxy.setItems(data.data);
          proxy.setCount(data.pagination.count);
          return data.data;
        }));
      }

      function clear() {
        $scope.filters = {};
        search();
      }
    }

    PatientListController.prototype = Object.create(ListController.prototype);

    return PatientListController;
  });
})();
