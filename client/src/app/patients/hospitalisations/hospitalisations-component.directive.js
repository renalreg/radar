(function() {
  'use strict';

  var app = angular.module('radar.patients.hospitalisations');

  app.factory('HospitalisationPermission', function(PatientFacilityDataPermission) {
    return PatientFacilityDataPermission;
  });

  app.factory('HospitalisationsController', function(ListDetailController, HospitalisationPermission) {
    function HospitalisationsController($scope, $injector, $q, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: $injector.instantiate(HospitalisationPermission, {patient: $scope.patient})
        }
      });

      var items = [];

      $q.all([
        store.findMany('hospitalisations', {patientId: $scope.patient.id}).then(function(hospitalisations) {
          items = hospitalisations;
        })
      ]).then(function() {
        self.load(items);
      });

      $scope.create = function() {
        var item = store.create('hospitalisations', {patientId: $scope.patient.id});
        self.edit(item);
      };
    }

    HospitalisationsController.prototype = Object.create(ListDetailController.prototype);

    return HospitalisationsController;
  });

  app.directive('hospitalisationsComponent', function(HospitalisationsController) {
    return {
      scope: {
        patient: '='
      },
      controller: HospitalisationsController,
      templateUrl: 'app/patients/hospitalisations/hospitalisations-component.html'
    };
  });
})();
