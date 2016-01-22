(function() {
  'use strict';

  var app = angular.module('radar.patients.medications');

  app.factory('ConsultantPermission', ['AdminPermission', function(AdminPermission) {
    return AdminPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    ConsultantPermission,
    firstPromise,
    $injector,
    store
  ) {
    function ConsultantsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new ConsultantPermission($scope.patient)
        }
      });

      self.load(store.findMany('consultants'));

      $scope.create = function() {
        var item = store.create('consultants');
        self.edit(item);
      };
    }

    ConsultantsController.$inject = ['$scope'];
    ConsultantsController.prototype = Object.create(ModelListDetailController.prototype);

    return ConsultantsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'ConsultantPermission',
    'firstPromise',
    '$injector',
    'store'
  ];

  app.factory('ConsultantsController', controllerFactory);

  app.directive('consultantsComponent', ['ConsultantsController', function(ConsultantsController) {
    return {
      controller: ConsultantsController,
      templateUrl: 'app/consultants/consultants-component.html'
    };
  }]);
})();
