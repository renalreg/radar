(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  function factory($q) {
    /** Controller for viewing a list of items */
    function ListController($scope) {
      this.scope = $scope;

      this.scope.loading = true;
      this.scope.items = [];
    }

    ListController.$inject = ['$scope'];

    ListController.prototype.load = function(promise) {
      var self = this;

      self.scope.loading = true;

      return $q.when(promise).then(function(items) {
        self.scope.loading = false;
        self.scope.items = items;
      });
    };

    return ListController;
  }

  factory.$inject = ['$q'];

  app.factory('ListController', factory);
})();
