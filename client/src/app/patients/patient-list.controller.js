(function() {
  'use strict';

  var app = angular.module('radar.patients');

  app.factory('PatientListController', function(ListController, $injector) {
    function PatientListController($scope, store) {
      $injector.invoke(ListController, this, {$scope: $scope});

      this.load(store.findMany('patients'));
    }

    PatientListController.prototype = Object.create(ListController.prototype);

    return PatientListController;
  });
})();
