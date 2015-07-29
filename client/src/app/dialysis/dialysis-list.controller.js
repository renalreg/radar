(function() {
  'use strict';

  var app = angular.module('radar.dialysis');

  app.controller('DialysisListController', function($scope, items, patient) {
    $scope.items = items;
    $scope.save = save;

    create();

    function create() {
      $scope.item = {
        patientId: patient.id,
        facilityId: 1,
        dialysisTypeId: 1
      };
    }

    function save() {
      $scope.items.post($scope.item).then(function(item) {
        $scope.items.push(item);
        create();
      });
    }
  });
})();
