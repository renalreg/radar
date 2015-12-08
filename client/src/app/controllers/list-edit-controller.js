(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  function factory(_, $q) {
    /** Controller for viewing and editing a list of items */
    function ListEditController($scope) {
      this.scope = $scope;

      this.scope.loading = true;
      this.scope.items = [];

      this.scope.append = angular.bind(this, this.append);
      this.scope.remove = angular.bind(this, this.remove);

      this.scope.removeEnabled = angular.bind(this, this.removeEnabled);
      this.scope.removePermission = angular.bind(this, this.removePermission);
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

    ListEditController.prototype.removeEnabled = function() {
      return true;
    };

    ListEditController.prototype.removePermission = function() {
      return true;
    };

    return ListEditController;
  }

  factory.$inject = ['_', '$q'];

  app.factory('ListEditController', factory);
})();
