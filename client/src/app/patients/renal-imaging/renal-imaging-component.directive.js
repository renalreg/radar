(function() {
  'use strict';

  var app = angular.module('radar.patients.renalImaging');

  app.factory('RenalImagingPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  app.factory('RenalImagingController', ['ListDetailController', 'RenalImagingPermission', 'firstPromise', '$injector', 'store', function(ListDetailController, RenalImagingPermission, firstPromise, $injector, store) {
    function RenalImagingController($scope) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new RenalImagingPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('renal-imaging', {patient: $scope.patient.id}),
        store.findMany('renal-imaging-types').then(function(imagingTypes) {
          $scope.imagingTypes = imagingTypes;
        }),
        store.findMany('renal-imaging-kidney-types').then(function(kidneyTypes) {
          $scope.kidneyTypes = kidneyTypes;
        })
      ]));

      $scope.create = function() {
        var item = store.create('renal-imaging', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    RenalImagingController.$inject = ['$scope'];
    RenalImagingController.prototype = Object.create(ListDetailController.prototype);

    return RenalImagingController;
  }]);

  app.directive('renalImagingComponent', ['RenalImagingController', function(RenalImagingController) {
    return {
      scope: {
        patient: '='
      },
      controller: RenalImagingController,
      templateUrl: 'app/patients/renal-imaging/renal-imaging-component.html'
    };
  }]);
})();
