(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('SaltWastingClinicalFeaturesPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelDetailController,
    SaltWastingClinicalFeaturesPermission,
    $injector,
    store
  ) {
    function SaltWastingClinicalFeaturesController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
        $scope: $scope,
        params: {
          permission: new SaltWastingClinicalFeaturesPermission($scope.patient)
        }
      });

      self.load(store.findFirst('salt-wasting-clinical-features', {patient: $scope.patient.id})).then(function() {
        self.view();
      });

      $scope.create = function() {
        var item = store.create('salt-wasting-clinical-features', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    SaltWastingClinicalFeaturesController.$inject = ['$scope'];
    SaltWastingClinicalFeaturesController.prototype = Object.create(ModelDetailController.prototype);

    return SaltWastingClinicalFeaturesController;
  }

  controllerFactory.$inject = [
    'ModelDetailController',
    'SaltWastingClinicalFeaturesPermission',
    '$injector',
    'store'
  ];

  app.factory('SaltWastingClinicalFeaturesController', controllerFactory);

  app.directive('saltWastingClinicalFeaturesComponent', ['SaltWastingClinicalFeaturesController', function(SaltWastingClinicalFeaturesController) {
    return {
      scope: {
        patient: '='
      },
      controller: SaltWastingClinicalFeaturesController,
      templateUrl: 'app/patients/salt-wasting/clinical-features-component.html'
    };
  }]);
})();
