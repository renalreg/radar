(function() {
  'use strict';

  var app = angular.module('radar.patients.pregnancies');

  app.factory('PregnancyPermission', ['PatientSourceGroupObjectPermission', function(PatientSourceGroupObjectPermission) {
    return PatientSourceGroupObjectPermission;
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
        store.findMany('pregnancies', {patient: $scope.patient.id}),
        store.findMany('pregnancy-outcomes').then(function(outcomes) {
          $scope.outcomes = outcomes;
        }),
        store.findMany('pregnancy-delivery-methods').then(function(deliveryMethods) {
          $scope.deliveryMethods = deliveryMethods;
        }),
        store.findMany('pregnancy-pre-eclampsia-types').then(function(preEclampsiaTypes) {
          $scope.preEclampsiaTypes = preEclampsiaTypes;
        })
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
