(function() {
  'use strict';

  var app = angular.module('radar.patients.fetalUltrasounds');

  app.factory('FetalUltrasoundPermission', ['PatientSourceGroupObjectPermission', function(PatientSourceGroupObjectPermission) {
    return PatientSourceGroupObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    FetalUltrasoundPermission,
    firstPromise,
    $injector,
    store
  ) {
    function FetalUltrasoundsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new FetalUltrasoundPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('fetal-ultrasounds', {patient: $scope.patient.id}),
        store.findMany('fetal-ultrasound-liquor-volumes').then(function(liquorVolumes) {
          $scope.liquorVolumes = liquorVolumes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('fetal-ultrasounds', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    FetalUltrasoundsController.$inject = ['$scope'];
    FetalUltrasoundsController.prototype = Object.create(ModelListDetailController.prototype);

    return FetalUltrasoundsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'FetalUltrasoundPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('FetalUltrasoundsController', controllerFactory);

  app.directive('fetalUltrasoundsComponent', ['FetalUltrasoundsController', function(FetalUltrasoundsController) {
    return {
      scope: {
        patient: '='
      },
      controller: FetalUltrasoundsController,
      templateUrl: 'app/patients/fetal-ultrasounds/fetal-ultrasounds-component.html'
    };
  }]);
})();
