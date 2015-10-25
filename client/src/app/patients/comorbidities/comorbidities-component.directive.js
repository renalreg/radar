(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.factory('ComorbidityPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  function controllerFactory(
    ListDetailController,
    ComorbidityPermission,
    firstPromise,
    $injector,
    store
  ) {
    function ComorbiditiesController($scope) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new ComorbidityPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('comorbidities', {patient: $scope.patient.id}),
        store.findMany('comorbidity-disorders').then(function(disorders) {
          $scope.disorders = disorders;
        })
      ]));

      $scope.create = function() {
        var item = store.create('comorbidities', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    ComorbiditiesController.$inject = ['$scope'];
    ComorbiditiesController.prototype = Object.create(ListDetailController.prototype);

    return ComorbiditiesController;
  }

  controllerFactory.$inject = [
    'ListDetailController',
    'ComorbidityPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('ComorbiditiesController', controllerFactory);

  app.directive('comorbiditiesComponent', ['ComorbiditiesController', function(ComorbiditiesController) {
    return {
      scope: {
        patient: '='
      },
      controller: ComorbiditiesController,
      templateUrl: 'app/patients/comorbidities/comorbidities-component.html'
    };
  }]);
})();
