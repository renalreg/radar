(function() {
  'use strict';

  var app = angular.module('radar.patients.results');

  app.factory('ResultPermission', ['PatientSourceObjectPermission', function(PatientSourceObjectPermission) {
    return PatientSourceObjectPermission;
  }]);

  function controllerFactory(
    ModelListDetailController,
    ResultPermission,
    firstPromise,
    $injector,
    store,
    _,
    transformResultsForGraph,
    transformResultsForTable
  ) {
    var TABLE = 0;
    var GRAPH = 1;

    // Remember selected observations
    var selectedObservations = [];

    function ResultsController($scope) {
      var self = this;

      $injector.invoke(ModelListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new ResultPermission($scope.patient)
        }
      });

      var currentView = TABLE;
      $scope.selectedObservations = selectedObservations;
      $scope.selectedObservation = null;

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

      // Reset the result value when the observation changes
      $scope.$watch('item.observation', function(oldValue, newValue) {
        if ($scope.editing && oldValue != newValue) {
          $scope.item.value = null;
        }
      });

      $scope.create = function() {
        var item = store.create('results', {
          patient: $scope.patient.id,
          observation: $scope.selectedObservation
        });

        self.edit(item);
      };

      $scope.saveAndAddAnother = function() {
        return self.save().then(function(item) {
          self.edit(store.create('results', {
            patient: item.patient,
            sourceGroup: item.sourceGroup,
            observation: item.observation
          }));

          return item;
        });
      };

      $scope.viewTable = function() {
        currentView = TABLE;
      };

      $scope.viewGraph = function() {
        currentView = GRAPH;
      };

      $scope.viewingTable = function() {
        return currentView === TABLE;
      };

      $scope.viewingGraph = function() {
        return currentView === GRAPH;
      };
    }

    ResultsController.$inject = ['$scope'];
    ResultsController.prototype = Object.create(ModelListDetailController.prototype);

    ResultsController.prototype.groupResults = function() {
      var results = this.scope.items;
      var observations = this.scope.selectedObservations;

      this.scope.groupedResults = transformResultsForTable(results, observations);
      this.scope.graphs = transformResultsForGraph(results, observations);
    };

    ResultsController.prototype.load = function(promise) {
      var self = this;

      return ModelListDetailController.prototype.load.call(this, promise).then(function(items) {
        self.groupResults();
        return items;
      });
    };

    ResultsController.prototype.save = function() {
      var self = this;

      return ModelListDetailController.prototype.save.call(this).then(function(item) {
        self.groupResults();
        return item;
      });
    };

    ResultsController.prototype.remove = function(item) {
      var self = this;

      return ModelListDetailController.prototype.remove.call(this, item).then(function(item) {
        self.groupResults();
        return item;
      });
    };

    return ResultsController;
  }

  controllerFactory.$inject = [
    'ModelListDetailController',
    'ResultPermission',
    'firstPromise',
    '$injector',
    'store',
    '_',
    'transformResultsForGraph',
    'transformResultsForTable'
  ];

  app.factory('ResultsController', controllerFactory);

  app.directive('resultsComponent', ['ResultsController', function(ResultsController) {
    return {
      scope: {
        patient: '='
      },
      controller: ResultsController,
      templateUrl: 'app/patients/results/results-component.html'
    };
  }]);
})();
