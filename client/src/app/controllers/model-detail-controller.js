(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  app.factory('ModelDetailController', ['$q', '$window', 'GrantPermission', function($q, $window, GrantPermission) {
    function ModelDetailController($scope, params) {
      this.scope = $scope;

      if (params.createPermission) {
        this._createPermission = params.createPermission;
      } else if (params.permission) {
        this._createPermission = params.permission;
      } else {
        this._createPermission = new GrantPermission();
      }

      if (params.editPermission) {
        this._editPermission = params.editPermission;
      } else if (params.permission) {
        this._editPermission = params.permission;
      } else {
        this._editPermission = new GrantPermission();
      }

      if (params.removePermission) {
        this._removePermission = params.removePermission;
      } else if (params.permission) {
        this._removePermission = params.permission;
      } else {
        this._removePermission = new GrantPermission();
      }

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
      this.scope.createEnabled = angular.bind(this, this.createEnabled);
      this.scope.editEnabled = angular.bind(this, this.editEnabled);
      this.scope.removeEnabled = angular.bind(this, this.removeEnabled);
      this.scope.saveEnabled = angular.bind(this, this.saveEnabled);
      this.scope.cancelEnabled = angular.bind(this, this.cancelEnabled);

      this.scope.createPermission = angular.bind(this, this.createPermission);
      this.scope.editPermission = angular.bind(this, this.editPermission);
      this.scope.removePermission = angular.bind(this, this.removePermission);

      this.scope.createVisible = angular.bind(this, this.createVisible);
    }

    ModelDetailController.$inject = ['$scope', 'params'];

    ModelDetailController.prototype.load = function(promise) {
      var self = this;

      self.scope.loading = true;

      return $q.when(promise).then(function(item) {
        self.scope.item = item;
        self.scope.loading = false;
      });
    };

    ModelDetailController.prototype.discardChanges = function() {
      return $window.confirm('Discard unsaved changes?');
    };

    ModelDetailController.prototype.view = function(item) {
      if (item === undefined) {
        item = this.scope.item;
      }

      // Can't view unsaved item
      if (item !== null && item.getId() === null) {
        item = null;
      }

      var ok = !this.scope.editing ||
        this.scope.item === null ||
        !this.scope.item.isDirty() ||
        this.discardChanges();

      if (!ok) {
        return;
      }

      this.scope.viewing = true;
      this.scope.editing = false;
      this.scope.originalItem = null;
      this.scope.item = item;
    };

    ModelDetailController.prototype.edit = function(item) {
      var ok = !this.scope.editing ||
        !this.scope.item.isDirty() ||
        this.discardChanges();

      if (!ok) {
        return;
      }

      this.scope.viewing = false;
      this.scope.editing = true;
      this.scope.originalItem = item;
      this.scope.item = item.clone();
    };

    ModelDetailController.prototype.save = function() {
      var self = this;

      self.scope.saving = true;

      return this.scope.item.save()['finally'](function() {
        self.scope.saving = false;
      });
    };

    ModelDetailController.prototype.saveAndView = function() {
      var self = this;

      return self.save().then(function(item) {
        self.view(item);
      });
    };

    ModelDetailController.prototype.remove = function() {
      var self = this;

      self.scope.saving = true;

      return self.scope.item.remove()
        .then(function() {
          self.scope.originalItem = null;
          self.scope.item = null;
          self.view(null);
        })
        ['finally'](function() {
          self.scope.saving = false;
        });
    };

    ModelDetailController.prototype.viewEnabled = function() {
      return this.scope.item !== null &&
        this.scope.item.getId() !== null &&
        !this.scope.saving;
    };

    ModelDetailController.prototype.createEnabled = function() {
      return this.scope.item === null && !this.scope.saving;
    };

    ModelDetailController.prototype.editEnabled = function() {
      return this.scope.item !== null &&
        this.scope.item.getId() !== null &&
        !this.scope.saving;
    };

    ModelDetailController.prototype.removeEnabled = function() {
      return this.scope.item !== null &&
        this.scope.item.getId() !== null &&
        !this.scope.saving;
    };

    ModelDetailController.prototype.saveEnabled = function() {
      return this.scope.item !== null && !this.scope.saving;
    };

    ModelDetailController.prototype.cancelEnabled = function() {
      return !this.scope.saving;
    };

    ModelDetailController.prototype.createPermission = function() {
      return this._createPermission.hasPermission();
    };

    ModelDetailController.prototype.editPermission = function() {
      return this._editPermission.hasObjectPermission(this.scope.item);
    };

    ModelDetailController.prototype.removePermission = function() {
      return this._removePermission.hasObjectPermission(this.scope.item);
    };

    ModelDetailController.prototype.createVisible = function() {
      return this.scope.item === null;
    };

    return ModelDetailController;
  }]);
})();
