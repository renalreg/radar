(function() {
  'use strict';

  var app = angular.module('radar.renalImaging');

  app.directive('rrRenalImagingEditor', function() {
    return {
      restrict: 'A',
      scope: {
        patient: '='
      },
      templateUrl: 'app/renal-imaging/renal-imaging-editor.html',
      controller: 'RenalImagingEditorController'
    };
  });

  app.controller('RenalImagingEditorController', function($scope, RenalImagingService, ListService, DetailService) {
    $scope.list = new ListService(function() {
      return RenalImagingService.getList($scope.patient.id);
    });

    $scope.detail = new DetailService();

    $scope.create = create;
    $scope.modified = modified;
    $scope.remove = remove;
    $scope.save = save;
    $scope.cancel = cancel;

    create();

    function create() {
      var item = RenalImagingService.create({patientId: $scope.patient.id});
      console.log(item);
      $scope.detail.edit(item);
    }

    function modified() {
      return $scope.form.$dirty && $scope.detail.isModified();
    }

    function remove(item) {
      return $scope.list.remove(item);
    }

    function save() {
      $scope.detail.save().then(function(item) {
        $scope.list.add(item);
        create();
      }).finally(function() {
        $scope.form.$setPristine();
      });
    }

    function cancel() {
      $scope.form.$setPristine();
      create();
    }
  });
})();

