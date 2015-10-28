(function() {
  'use strict';

  var app = angular.module('radar.patients.meta');

  app.factory('PatientMetaPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelDetailController,
    PatientMetaPermission,
    $injector
  ) {
    function PatientMetaController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
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
    PatientMetaController.prototype = Object.create(ModelDetailController.prototype);

    return PatientMetaController;
  }

  controllerFactory.$inject = ['ModelDetailController', 'PatientMetaPermission', '$injector'];

  app.factory('PatientMetaController', controllerFactory);

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
