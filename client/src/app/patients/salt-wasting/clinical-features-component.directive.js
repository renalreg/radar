(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('SaltWastingClinicalFeaturesPermission', function(PatientDataPermission) {
    return PatientDataPermission;
  });

  app.factory('SaltWastingClinicalFeaturesController', function(DetailController, SaltWastingClinicalFeaturesPermission) {
    function SaltWastingClinicalFeaturesController($scope, $injector, store) {
      var self = this;

      $injector.invoke(DetailController, self, {
        $scope: $scope,
        params: {
          permission: new SaltWastingClinicalFeaturesPermission($scope.patient)
        }
      });

      self.load(store.findMany('salt-wasting-clinical-features', {patient: $scope.patient.id}).then(function(results) {
        if (results.length) {
          return results[0];
        } else {
          return null;
        }
      })).then(function() {
        self.view();
      });

      $scope.create = function() {
        var item = store.create('salt-wasting-clinical-features', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    SaltWastingClinicalFeaturesController.prototype = Object.create(DetailController.prototype);

    return SaltWastingClinicalFeaturesController;
  });

  app.directive('saltWastingClinicalFeaturesComponent', function(SaltWastingClinicalFeaturesController) {
    return {
      scope: {
        patient: '='
      },
      controller: SaltWastingClinicalFeaturesController,
      templateUrl: 'app/patients/salt-wasting/clinical-features-component.html'
    };
  });
})();
