(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('ResultPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  function controllerFactory(
    ListDetailController,
    ResultPermission,
    firstPromise,
    $injector,
    store,
    _
  ) {
    function ResultListController($scope) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new ResultPermission($scope.patient)
        }
      });

      $scope.resultSpecs = [];

      var resultGroupSpecsPromise = store.findMany('result-group-specs').then(function(resultGroupSpecs) {
        $scope.resultGroupSpecs = resultGroupSpecs;
      });

      var resultSpecsSelected = false;

      $scope.$watchCollection('resultSpecs', function(resultSpecs) {
        var promise;

        if (resultSpecs.length) {
          resultSpecsSelected = true;

          var resultCodes = [];

          _.forEach(resultSpecs, function(x) {
            resultCodes.push(x.code);
          });

          var resultCodesStr = resultCodes.join(',');

          promise = store.findMany('result-groups', {patient: $scope.patient.id, resultCodes: resultCodesStr});
        } else {
          promise = [];
        }

        if (resultSpecsSelected) {
          self.load(firstPromise([
            promise,
            resultGroupSpecsPromise
          ]));
        }
      });

      $scope.create = function() {
        var item = store.create('result-groups', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    ResultListController.$inject = ['$scope'];
    ResultListController.prototype = Object.create(ListDetailController.prototype);

    ResultListController.prototype.groupItems = function() {
      var self = this;

      var items = self.scope.items;
      var groupedItems = [];
      var currentKey = null;
      var current = null;

      _.forEach(items, function(x) {
        var meta = _.any(self.scope.resultSpecs, function(x) {
          return x.meta;
        });

        var key = x.dataSource.id + '.' + x.date;

        // Rows with metadata (e.g. pre/post dialysis) shouldn't be grouped with other result groups
        if (key !== currentKey || current === null || meta) {
          currentKey = key;
          current = {
            date: x.date,
            dataSource: x.dataSource,
            results: {}
          };
          groupedItems.push(current);
        }

        _.forEach(self.scope.resultSpecs, function(resultSpec) {
          var code = resultSpec.code;
          var value = x.results[code];

          if (value === undefined) {
            return;
          }

          if (current[code] !== undefined) {
            current = {
              date: x.date,
              dataSource: x.dataSource,
              results: {}
            };
            groupedItems.push(current);
          }

          current.results[code] = x;
        });

        // Force a new row
        if (meta) {
          current = null;
        }
      });

      this.scope.groupedItems = groupedItems;
    };

    ResultListController.prototype.load = function(promise) {
      var self = this;

      return ListDetailController.prototype.load.call(this, promise).then(function(items) {
        self.groupItems();
        return items;
      });
    };

    ResultListController.prototype.save = function() {
      var self = this;

      return ListDetailController.prototype.save.call(this).then(function(item) {
        self.groupItems();
        return item;
      });
    };

    ResultListController.prototype.remove = function(item) {
      var self = this;

      return ListDetailController.prototype.remove.call(this, item).then(function(item) {
        self.groupItems();
        return item;
      });
    };

    return ResultListController;
  }

  controllerFactory.$inject = [
    'ListDetailController',
    'ResultPermission',
    'firstPromise',
    '$injector',
    'store',
    '_'
  ];

  app.factory('ResultListController', controllerFactory);

  app.directive('resultListComponent', ['ResultListController', function(ResultListController) {
    return {
      scope: {
        patient: '='
      },
      controller: ResultListController,
      templateUrl: 'app/patients/results/result-list-component.html'
    };
  }]);
})();
