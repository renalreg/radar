(function() {
  'use strict';

  var app = angular.module('radar.patients.pregnancies');

  app.factory('PregnancyPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    PregnancyPermission,
    firstPromise,
    $injector,
    store
  ) {
    function PregnanciesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PregnancyPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('pregnancies', {patient: $scope.patient.id})
      ]));

      $scope.create = function() {
        var item = store.create('pregnancies', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PregnanciesController.$inject = ['$scope'];
    PregnanciesController.prototype = Object.create(ModelListDetailController.prototype);

    return PregnanciesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PregnancyPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('PregnanciesController', controllerFactory);

  app.directive('pregnanciesComponent', ['PregnanciesController', function(PregnanciesController) {
    return {
      scope: {
        patient: '='
      },
      controller: PregnanciesController,
      templateUrl: 'app/patients/pregnancies/pregnancies-component.html'
    };
  }]);
})();
