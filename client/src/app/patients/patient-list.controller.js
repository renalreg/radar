(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientListController', function(ListController, $injector, ListHelperProxy) {
    function PatientListController($scope, store) {
      var self = this;

      $injector.invoke(ListController, self, {$scope: $scope});

      var proxy = new ListHelperProxy(function(ctrl, params) {
        self.load(store.findMany('patients', params, true).then(function(data) {
          ctrl.setItems(data.data);
          ctrl.setCount(data.pagination.count);
          return data.data;
        }));
      });
      proxy.load();

      $scope.proxy = proxy;
    }

    PatientListController.prototype = Object.create(ListController.prototype);

    return PatientListController;
  });
})();
