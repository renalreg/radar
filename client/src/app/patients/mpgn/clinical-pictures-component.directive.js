(function() {
  'use strict';

  var app = angular.module('radar.patients.mpgn');

  app.factory('MpgnClinicalPicturePermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    MpgnClinicalPicturePermission,
    $injector,
    store
  ) {
    function MpgnClinicalPicturesController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new MpgnClinicalPicturePermission($scope.patient)
        }
      });

      self.load(store.findMany('mpgn-clinical-pictures', {patient: $scope.patient.id}));

      $scope.create = function() {
        var item = store.create('mpgn-clinical-pictures', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    MpgnClinicalPicturesController.$inject = ['$scope'];
    MpgnClinicalPicturesController.prototype = Object.create(ModelListDetailController.prototype);

    return MpgnClinicalPicturesController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'MpgnClinicalPicturePermission',
    '$injector',
    'store'
  ];

  app.factory('MpgnClinicalPicturesController', controllerFactory);

  app.directive('mpgnClinicalPicturesComponent', ['MpgnClinicalPicturesController', function(MpgnClinicalPicturesController) {
    return {
      scope: {
        patient: '='
      },
      controller: MpgnClinicalPicturesController,
      templateUrl: 'app/patients/mpgn/clinical-pictures-component.html'
    };
  }]);
})();
