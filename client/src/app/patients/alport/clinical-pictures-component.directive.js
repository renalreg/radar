(function() {
  'use strict';

  var app = angular.module('radar.patients.alport');

  app.factory('AlportClinicalPicturePermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    AlportClinicalPicturePermission,
    firstPromise,
    $injector,
    store
  ) {
    function AlportClinicalPicturesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new AlportClinicalPicturePermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('alport-clinical-pictures', {patient: $scope.patient.id}),
        store.findMany('alport-deafness-options').then(function(deafnessOptions) {
          $scope.deafnessOptions = deafnessOptions;
        })
      ]));

      $scope.create = function() {
        var item = store.create('alport-clinical-pictures', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    AlportClinicalPicturesController.$inject = ['$scope'];
    AlportClinicalPicturesController.prototype = Object.create(ModelListDetailController.prototype);

    return AlportClinicalPicturesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'AlportClinicalPicturePermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('AlportClinicalPicturesController', controllerFactory);

  app.directive('alportClinicalPicturesComponent', ['AlportClinicalPicturesController', function(AlportClinicalPicturesController) {
    return {
      scope: {
        patient: '='
      },
      controller: AlportClinicalPicturesController,
      templateUrl: 'app/patients/alport/clinical-pictures-component.html'
    };
  }]);
})();
