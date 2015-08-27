(function() {
  'use strict';

  var app = angular.module('radar.dialysis');

  app.factory('DialysisController', function(ListDetailController) {
    function DialysisController($scope, $injector, $q, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {$scope: $scope});

      var items = [];

      $q.all([
        store.findMany('dialysis', {patientId: $scope.patient.id}).then(function(serverItems) {
          items = serverItems;
        }),
        store.findMany('dialysis-types').then(function(items) {
          $scope.dialysisTypes = items;
        })
      ]).then(function() {
        self.load(items);
      });

      $scope.create = function() {
        var item = store.create('dialysis', {patientId: $scope.patient.id, dialysisTypeId: 1, facilityId: 1});
        self.edit(item);
      };

      $scope.createPermission = function() {
        return true;
      };

      $scope.editPermission = function(item) {
        return true;
      };

      $scope.removePermission = function(item) {
        return true;
      };
    }

    DialysisController.prototype = Object.create(ListDetailController.prototype);

    return DialysisController;
  });

  app.directive('dialysisComponent', function(DialysisController) {
    // TODO disable save button when $invalid

    return {
      scope: {
        patient: '='
      },
      controller: DialysisController,
      templateUrl: 'app/dialysis/dialysis-component.html'
    };
  });
})();
