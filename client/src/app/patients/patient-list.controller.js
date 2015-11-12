(function() {
  'use strict';

  var app = angular.module('radar.patients');

  function controllerFactory(
    ListController,
    $injector,
    ListHelperProxy,
    firstPromise,
    store
  ) {
    function PatientListController($scope) {
      var self = this;

      $injector.invoke(ListController, self, {$scope: $scope});

      var defaultFilters = {
        isActive: true
      };
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

        self.load(firstPromise([
          store.findMany('patients', params, true).then(function(data) {
            proxy.setItems(data.data);
            proxy.setCount(data.pagination.count);
            $scope.count = data.pagination.count;
            return data.data;
          }),
          store.findMany('genders').then(function(genders) {
            $scope.genders = genders;
          })
        ]));
      }

      function clear() {
        $scope.filters = angular.copy(defaultFilters);
        search();
      }
    }

    PatientListController.$inject = ['$scope'];
    PatientListController.prototype = Object.create(ListController.prototype);

    return PatientListController;
  }

  controllerFactory.$inject = [
    'ListController',
    '$injector',
    'ListHelperProxy',
    'firstPromise',
    'store'
  ];

  app.factory('PatientListController', controllerFactory);
})();