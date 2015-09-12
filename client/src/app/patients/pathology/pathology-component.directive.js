(function() {
  'use strict';

  var app = angular.module('radar.patients.pathology');

  app.factory('PathologyPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  });

  app.factory('PathologyController', function(ListDetailController, PathologyPermission) {
    function PathologyController($scope, $injector, store) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PathologyPermission($scope.patient)
        }
      });

      self.load(store.findMany('pathology', {patient: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('pathology', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    PathologyController.prototype = Object.create(ListDetailController.prototype);

    return PathologyController;
  });

  app.directive('pathologyComponent', function(PathologyController) {
    return {
      scope: {
        patient: '='
      },
      controller: PathologyController,
      templateUrl: 'app/patients/pathology/pathology-component.html'
    };
  });
})();
