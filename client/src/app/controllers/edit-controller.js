(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  app.factory('EditController', function($q) {
    function EditController($scope) {
      this.scope = $scope;

      this.scope.loading = true;
      this.scope.item = null;

      this.scope.save = angular.bind(this, this.save);
      this.scope.saveEnabled = angular.bind(this, this.saveEnabled);
    }

    EditController.prototype.load = function(promise) {
      var self = this;

      self.scope.loading = true;

      return $q.when(promise).then(function(item) {
        self.scope.item = item;
        self.scope.loading = false;
      });
    };

    EditController.prototype.save = function() {
      var self = this;

      self.scope.saving = true;

      return self.scope.item.save().finally(function() {
        self.scope.saving = false;
      });
    };

    EditController.prototype.saveEnabled = function() {
      return this.scope.item !== null && !this.scope.item.isSaving;
    };

    return EditController;
  });
})();
