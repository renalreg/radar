(function() {
  'use strict';

  var app = angular.module('radar.patients.hnf1b');

  app.factory('Hnf1bClinicalPicturePermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    Hnf1bClinicalPicturePermission,
    firstPromise,
    $injector,
    store
  ) {
    function Hnf1bClinicalPicturesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new Hnf1bClinicalPicturePermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('hnf1b-clinical-pictures', {patient: $scope.patient.id}),
        store.findMany('hnf1b-diabetes-types').then(function(diabetesTypes) {
          $scope.diabetesTypes = diabetesTypes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('hnf1b-clinical-pictures', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    Hnf1bClinicalPicturesController.$inject = ['$scope'];
    Hnf1bClinicalPicturesController.prototype = Object.create(ModelListDetailController.prototype);

    return Hnf1bClinicalPicturesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'Hnf1bClinicalPicturePermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('Hnf1bClinicalPicturesController', controllerFactory);

  app.directive('hnf1bClinicalPicturesComponent', ['Hnf1bClinicalPicturesController', function(Hnf1bClinicalPicturesController) {
    return {
      scope: {
        patient: '='
      },
      controller: Hnf1bClinicalPicturesController,
      templateUrl: 'app/patients/hnf1b/clinical-pictures-component.html'
    };
  }]);
})();
