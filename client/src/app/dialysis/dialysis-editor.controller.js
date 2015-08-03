/* global humps */

(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('DialysisEditorController', function($scope, DialysisService, DialysisTypeService) {
    DialysisService.getList($scope.patient.id).then(function(items) {
      $scope.items = items;
    });

    DialysisTypeService.getDialysisTypes().then(function(dialysisTypes) {
      $scope.dialysisTypes = dialysisTypes;
    });

    $scope.save = save;
    $scope.edit = edit;

    create();

    function create() {
      $scope.item = DialysisService.create({
        patientId: $scope.patient.id
      });
    }

    function edit(item) {
      $scope.item = item;
    }

    function save() {
      $scope.errors = {};

      $scope.item.$save().then(function(item) {
        $scope.form.$setPristine();
        create();
      }, function(response) {
        if (response.status === 422) {
          $scope.errors = humps.camelizeKeys(response.data.errors);
        }
      });
    }
  });
})();
