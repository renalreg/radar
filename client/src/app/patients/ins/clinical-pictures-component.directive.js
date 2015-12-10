(function() {
  'use strict';

  var app = angular.module('radar.patients.ins');

  app.factory('InsClinicalPicturePermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    InsClinicalPicturePermission,
    $injector,
    store
  ) {
    function InsClinicalPicturesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new InsClinicalPicturePermission($scope.patient)
        }
      });

      self.load(store.findMany('ins-clinical-pictures', {patient: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('ins-clinical-pictures', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    InsClinicalPicturesController.$inject = ['$scope'];
    InsClinicalPicturesController.prototype = Object.create(ModelListDetailController.prototype);

    return InsClinicalPicturesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'InsClinicalPicturePermission',
    '$injector',
    'store'
  ];

  app.factory('InsClinicalPicturesController', controllerFactory);

  app.directive('insClinicalPicturesComponent', ['InsClinicalPicturesController', function(InsClinicalPicturesController) {
    return {
      scope: {
        patient: '='
      },
      controller: InsClinicalPicturesController,
      templateUrl: 'app/patients/ins/clinical-pictures-component.html'
    };
  }]);
})();
