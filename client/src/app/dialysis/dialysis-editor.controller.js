(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('DialysisEditorController', function($scope, DialysisService, DialysisTypeService, lodash, humps, $q, $timeout) {
    $scope.sortBy = 'id';
    $scope.reverse = false;
    $scope.page = 1;
    $scope.perPage = 3;

    DialysisService.getList($scope.patient.id).then(function(items) {
      $scope.items = items;
    });

    DialysisTypeService.getDialysisTypes().then(function(dialysisTypes) {
      $scope.dialysisTypes = dialysisTypes;
    });

    $scope.$watch('items', filter);
    $scope.$watch('filteredItems', sort);
    $scope.$watch('sortBy', sort);
    $scope.$watch('reverse', sort);
    $scope.$watch('sortedItems', paginate);
    $scope.$watch('page', paginate);
    $scope.$watch('perPage', paginate);

    var original = null;

    $scope.save = save;
    $scope.edit = edit;
    $scope.remove = remove;
    $scope.cancel = cancel;
    $scope.modified = modified;

    create();
    sort();
    paginate();

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

    function filter() {
      $scope.filteredItems = $scope.items;
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

    function sort() {
      $scope.page = 1;

      var sortedItems = lodash.sortBy($scope.items, $scope.sortBy);

      if ($scope.reverse) {
        sortedItems.reverse();
      }

      $scope.sortedItems = sortedItems;
    }

    function paginate() {
      var startIndex = ($scope.page - 1) * $scope.perPage;
      var endIndex = $scope.page * $scope.perPage;
      $scope.paginatedItems = lodash.slice($scope.sortedItems, startIndex, endIndex);
    }
  });
})();
