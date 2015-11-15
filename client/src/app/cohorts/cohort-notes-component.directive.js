(function() {
  'use strict';

  var app = angular.module('radar.cohorts');

  function controllerFactory(
    ModelDetailController,
    $injector,
    store
  ) {
    function CohortNotesController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
        $scope: $scope,
        params: {}
      });

      self.load($scope.cohort).then(function() {
        self.view();
      });
    }

    CohortNotesController.$inject = ['$scope'];
    CohortNotesController.prototype = Object.create(ModelDetailController.prototype);

    return CohortNotesController;
  }

  controllerFactory.$inject = [
    'ModelDetailController',
    '$injector',
    'store'
  ];

  app.factory('CohortNotesController', controllerFactory);

  app.directive('cohortNotesComponent', ['CohortNotesController', function(CohortNotesController) {
    return {
      scope: {
        cohort: '='
      },
      controller: CohortNotesController,
      templateUrl: 'app/cohorts/cohort-notes-component.html'
    };
  }]);
})();
