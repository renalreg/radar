(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  app.factory('ListController', function($q) {
    function ListController($scope) {
      this.scope = $scope;

      this.scope.loading = true;
      this.scope.items = [];
    }

    ListController.prototype.load = function(promise) {
      var self = this;

      self.scope.loading = true;

      return $q.when(promise).then(function(items) {
        self.scope.loading = false;
        self.scope.items = items;
      });
    };

    return ListController;
  });
})();
