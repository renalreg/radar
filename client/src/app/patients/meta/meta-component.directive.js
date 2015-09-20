(function() {
  'use strict';

  var app = angular.module('radar.patients.meta');

  app.factory('PatientMetaPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  app.factory('PatientMetaController', ['DetailController', 'PatientMetaPermission', '$injector', function(DetailController, PatientMetaPermission, $injector) {
    function PatientMetaController($scope) {
      var self = this;

      $injector.invoke(DetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientMetaPermission($scope.patient)
        }
      });

      self.load($scope.patient).then(function() {
        self.view();
      });
    }

    PatientMetaController.$inject = ['$scope'];
    PatientMetaController.prototype = Object.create(DetailController.prototype);

    return PatientMetaController;
  }]);

  app.directive('patientMetaComponent', ['PatientMetaController', function(PatientMetaController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientMetaController,
      templateUrl: 'app/patients/meta/meta-component.html'
    };
  }]);
})();
