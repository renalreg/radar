(function() {
  'use strict';

  var app = angular.module('radar.patients.pregnancy');

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
    function PregnancyController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PregnancyPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('pregnancy', {patient: $scope.patient.id})
      ]));

      $scope.create = function() {
        var item = store.create('pregnancy', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PregnancyController.$inject = ['$scope'];
    PregnancyController.prototype = Object.create(ModelListDetailController.prototype);

    return PregnancyController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'PregnancyPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('PregnancyController', controllerFactory);

  app.directive('pregnancyComponent', ['PregnancyController', function(PregnancyController) {
    return {
      scope: {
        patient: '='
      },
      controller: PregnancyController,
      templateUrl: 'app/patients/pregnancy/pregnancy-component.html'
    };
  }]);
})();
