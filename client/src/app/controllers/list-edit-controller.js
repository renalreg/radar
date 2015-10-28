(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  app.factory('ListEditController', ['_', '$q', function(_, $q) {
    function ListEditController($scope) {
      this.scope = $scope;

      this.scope.loading = true;
      this.scope.items = [];

      this.scope.append = angular.bind(this, this.append);
      this.scope.remove = angular.bind(this, this.remove);
    }

    ListEditController.$inject = ['$scope'];

    ListEditController.prototype.load = function(promise) {
      var self = this;

      self.scope.loading = true;
      self.scope.items = [];

      return $q.when(promise).then(function(items) {
        self.scope.loading = false;
        self.scope.items = items;
      });
    };

    ListEditController.prototype.append = function(item) {
      this.scope.items.push(item);
    };

    ListEditController.prototype.remove = function(item) {
      _.pull(this.scope.items, item);
    };

    return ListEditController;
  }]);
})();
