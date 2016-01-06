(function() {
  'use strict';

  var app = angular.module('radar.patients.metadata');

  app.factory('PatientMetadataPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelDetailController,
    PatientMetadataPermission,
    $injector
  ) {
    function PatientMetadataController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientMetadataPermission($scope.patient)
        }
      });

      self.load($scope.patient).then(function() {
        self.view();
      });
    }

    PatientMetadataController.$inject = ['$scope'];
    PatientMetadataController.prototype = Object.create(ModelDetailController.prototype);

    return PatientMetadataController;
  }

  controllerFactory.$inject = ['ModelDetailController', 'PatientMetadataPermission', '$injector'];

  app.factory('PatientMetadataController', controllerFactory);

  app.directive('patientMetadataComponent', ['PatientMetadataController', function(PatientMetadataController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientMetadataController,
      templateUrl: 'app/patients/metadata/metadata-component.html'
    };
  }]);
})();
