(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  app.factory('DetailController', function($q, $window) {
    function DetailController($scope) {
      this.scope = $scope;

      this.scope.loading = true;
      this.scope.viewing = false;
      this.scope.editing = false;
      this.scope.saving = false;
      this.scope.item = null;
      this.scope.originalItem = null;

      this.scope.view = angular.bind(this, this.view);
      this.scope.edit = angular.bind(this, this.edit);
      this.scope.save = angular.bind(this, this.save);
      this.scope.saveAndView = angular.bind(this, this.saveAndView);
      this.scope.remove = angular.bind(this, this.remove);
      this.scope.viewEnabled = angular.bind(this, this.viewEnabled);
      this.scope.editEnabled = angular.bind(this, this.editEnabled);
      this.scope.removeEnabled = angular.bind(this, this.removeEnabled);
      this.scope.saveEnabled = angular.bind(this, this.saveEnabled);
    }

    DetailController.prototype.load = function(promise) {
      var self = this;

      self.scope.loading = true;

      return $q.when(promise).then(function(item) {
        self.scope.item = item;
        self.scope.loading = false;
      });
    };

    DetailController.prototype.discardChanges = function() {
      return $window.confirm('Discard unsaved changes?');
    };

    DetailController.prototype.view = function() {
      var ok = !this.scope.editing ||
        this.scope.item === null ||
        !this.scope.item.isDirty() ||
        this.discardChanges();

      if (!ok) {
        return;
      }

      if (this.scope.editing) {
        if (this.scope.originalItem === null || this.scope.originalItem.getId() === null) {
          this.scope.item = null;
        } else {
          this.scope.item = this.scope.originalItem;
        }

        this.scope.originalItem = null;
      }

      this.scope.viewing = true;
      this.scope.editing = false;
    };

    DetailController.prototype.edit = function() {
      var ok = !this.scope.editing ||
        !this.scope.item.isDirty() ||
        this.discardChanges();

      if (!ok) {
        return;
      }

      this.scope.viewing = false;
      this.scope.editing = true;
      this.scope.originalItem = this.scope.item;
      this.scope.item = this.scope.item.clone();
    };

    DetailController.prototype.save = function() {
      var self = this;

      self.scope.saving = true;

      return this.scope.item.save().finally(function() {
        self.scope.saving = false;
      });
    };

    DetailController.prototype.saveAndView = function() {
      var self = this;

      return self.save().then(function() {
        self.view();
      });
    };

    DetailController.prototype.remove = function() {
      var self = this;

      self.scope.saving = true;

      return self.scope.item.remove()
        .then(function() {
          self.scope.originalItem = null;
          self.scope.item = null;
          self.view();
        })
        .finally(function() {
          self.scope.saving = false;
        });
    };

    DetailController.prototype.viewEnabled = function() {
      return this.scope.item !== null && !this.scope.saving;
    };

    DetailController.prototype.editEnabled = function() {
      return this.scope.item !== null && !this.scope.saving;
    };

    DetailController.prototype.removeEnabled = function() {
      return this.scope.item !== null && !this.scope.saving;
    };

    DetailController.prototype.saveEnabled = function() {
      return this.scope.item !== null && !this.scope.saving;
    };

    return DetailController;
  });
})();
