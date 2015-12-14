(function() {
  'use strict';

  var app = angular.module('radar.patients.fetalAnomalyScans');

  app.factory('FetalAnomalyScanPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    FetalAnomalyScanPermission,
    $injector,
    store
  ) {
    function FetalAnomalyScansController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new FetalAnomalyScanPermission($scope.patient)
        }
      });

      self.load(store.findMany('fetal-anomaly-scans', {patient: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('fetal-anomaly-scans', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    FetalAnomalyScansController.$inject = ['$scope'];
    FetalAnomalyScansController.prototype = Object.create(ModelListDetailController.prototype);

    return FetalAnomalyScansController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'FetalAnomalyScanPermission',
    '$injector',
    'store'
  ];

  app.factory('FetalAnomalyScansController', controllerFactory);

  app.directive('fetalAnomalyScansComponent', ['FetalAnomalyScansController', function(FetalAnomalyScansController) {
    return {
      scope: {
        patient: '='
      },
      controller: FetalAnomalyScansController,
      templateUrl: 'app/patients/fetal-anomaly-scans/fetal-anomaly-scans-component.html'
    };
  }]);
})();
