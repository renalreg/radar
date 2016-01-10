(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('ResultPermission', ['PatientDataSourceObjectPermission', function(PatientDataSourceObjectPermission) {
    return PatientDataSourceObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    ResultPermission,
    firstPromise,
    $injector,
    store,
    _
  ) {
    function ResultTableController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new ResultPermission($scope.patient)
        }
      });

      $scope.selectedObservations = [];

      $scope.$watchCollection('selectedObservations', function(selectedObservations) {
        var promise;

        if (selectedObservations.length) {
          var observationIds = _.map(selectedObservations, function(x) {
            return x.id;
          });

          observationIds = observationIds.join(',');

          promise = store.findMany('results', {patient: $scope.patient.id, observationIds: observationIds});
        } else {
          promise = [];
        }

        self.load(promise);
      });

      $scope.create = function() {
        var item = store.create('results', {patient: $scope.patient.id});
        self.edit(item);
      };
    }

    ResultTableController.$inject = ['$scope'];
    ResultTableController.prototype = Object.create(ModelListDetailController.prototype);

    ResultTableController.prototype.groupItems = function() {
      var self = this;

      var items = self.scope.items;

      var observationIds = _.map(self.scope.selectedObservations, function(x) {
        return x.id;
      });

      var groupedItems = [];
      var currentKey = null;
      var current = null;

      _.forEach(items, function(x) {
        var observationId = x.observation.id;

        if (_.indexOf(observationIds, observationId) === -1) {
          return;
        }

        var key = x.dataSource.id + '.' + x.date;

        if (
          key !== currentKey ||
          current === null ||
          current.results[observationId] !== undefined
        ) {
          currentKey = key;
          current = {
            date: x.date,
            dataSource: x.dataSource,
            results: {}
          };
          groupedItems.push(current);
        }

        current.results[observationId] = x;
      });

      this.scope.groupedItems = groupedItems;
    };

    ResultTableController.prototype.load = function(promise) {
      var self = this;

      return ModelListDetailController.prototype.load.call(this, promise).then(function(items) {
        self.groupItems();
        return items;
      });
    };

    ResultTableController.prototype.save = function() {
      var self = this;

      return ModelListDetailController.prototype.save.call(this).then(function(item) {
        self.groupItems();
        return item;
      });
    };

    ResultTableController.prototype.remove = function(item) {
      var self = this;

      return ModelListDetailController.prototype.remove.call(this, item).then(function(item) {
        self.groupItems();
        return item;
      });
    };

    return ResultTableController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'ResultPermission',
    'firstPromise',
    '$injector',
    'store',
    '_'
  ];

  app.factory('ResultTableController', controllerFactory);

  app.directive('resultTableComponent', ['ResultTableController', function(ResultTableController) {
    return {
      scope: {
        patient: '='
      },
      controller: ResultTableController,
      templateUrl: 'app/patients/results/result-table-component.html'
    };
  }]);
})();
