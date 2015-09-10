(function() {
  'use strict';

  var app = angular.module('radar.patients.hospitalisations');

  app.factory('HospitalisationPermission', function(PatientFacilityDataPermission) {
    return PatientFacilityDataPermission;
  });

  app.factory('HospitalisationsController', function(ListDetailController, HospitalisationPermission) {
    function HospitalisationsController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new HospitalisationPermission($scope.patient)
        }
      });

      self.load(store.findMany('hospitalisations', {patientId: $scope.patient.id}));

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
