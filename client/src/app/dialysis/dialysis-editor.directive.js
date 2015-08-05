(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrDialysisEditor', function() {
    return {
      restrict: 'A',
      scope: {
        patient: '='
      },
      templateUrl: 'app/dialysis/dialysis-editor.html',
      controller: 'DialysisEditorController'
    };
  });

  app.controller('DialysisEditorController', function($scope, DialysisService, DialysisTypeService, lodash, humps, $q, $timeout, $filter, ListService) {
    $scope.list = new ListService(function() {
      return DialysisService.getList($scope.patient.id);
    });

    DialysisTypeService.getDialysisTypes().then(function(dialysisTypes) {
      $scope.dialysisTypes = dialysisTypes;
    });

    var original = null;

    $scope.save = save;
    $scope.edit = edit;
    $scope.remove = remove;
    $scope.cancel = cancel;
    $scope.modified = modified;

    create();

    function create() {
      original = DialysisService.create({
        patientId: $scope.patient.id
      });
      $scope.item = angular.copy(original);
    }

    function edit(item) {
      original = item;
      $scope.item = angular.copy(item);
    }

    function remove(item) {
      if (item === original) {
        $scope.form.$setPristine();
        create();
      }

      var deferred = $q.defer();

      $timeout(function() {
        item.$delete().then(function() {
          lodash.pull($scope.items, item);
          deferred.resolve();
        });
      }, 1000);

      return deferred.promise;
    }

    function cancel() {
      $scope.form.$setPristine();
      create();
    }

    function modified() {
      return $scope.form.$dirty && !angular.equals(original, $scope.item);
    }

    function save() {
      var savedOriginal = original;

      $scope.errors = {};

      $scope.item.$save().then(function(item) {
        if (!savedOriginal.id) {
          $scope.items.push(savedOriginal);
        }

        angular.copy(item, savedOriginal);

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
