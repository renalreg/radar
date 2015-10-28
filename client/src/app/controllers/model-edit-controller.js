(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  app.factory('ModelEditController', ['$q', function($q) {
    function ModelEditController($scope) {
      this.scope = $scope;

      this.scope.loading = true;
      this.scope.item = null;
      this.scope.originalItem = null;

      this.scope.save = angular.bind(this, this.save);
      this.scope.saveEnabled = angular.bind(this, this.saveEnabled);
    }

    ModelEditController.$inject = ['$scope'];

    ModelEditController.prototype.load = function(promise) {
      var self = this;

      self.scope.loading = true;

      return $q.when(promise).then(function(item) {
        self.scope.originalItem = item;
        self.scope.item = item.clone();
        self.scope.loading = false;
      });
    };

    ModelEditController.prototype.save = function() {
      var self = this;

      self.scope.saving = true;

      return self.scope.item.save()
        .then(function(item) {
          self.scope.originalItem = item;
          self.scope.item = item.clone();
          return item;
        })
        ['finally'](function() {
          self.scope.saving = false;
        });
    };

    ModelEditController.prototype.saveEnabled = function() {
      return this.scope.item !== null && !this.scope.item.isSaving;
    };

    return ModelEditController;
  }]);
})();
