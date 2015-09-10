(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  app.factory('ListDetailController', function(_, $window, $q, noopPermission) {
    function ListDetailController($scope, params) {
      this.scope = $scope;

      if (params.createPermission) {
        this._createPermission = params.createPermission;
      } else if (params.permission) {
        this._createPermission = params.permission;
      } else {
        this._createPermission = noopPermission;
      }

      if (params.editPermission) {
        this._editPermission = params.editPermission;
      } else if (params.permission) {
        this._editPermission = params.permission;
      } else {
        this._editPermission = noopPermission;
      }

      if (params.removePermission) {
        this._removePermission = params.removePermission;
      } else if (params.permission) {
        this._removePermission = params.permission;
      } else {
        this._removePermission = noopPermission;
      }

      this.scope.loading = true;
      this.scope.saving = false;
      this.scope.viewing = false;
      this.scope.editing = false;
      this.scope.originalItem = null;
      this.scope.item = null;
      this.scope.items = [];

      this.scope.list = angular.bind(this, this.list);
      this.scope.view = angular.bind(this, this.view);
      this.scope.edit = angular.bind(this, this.edit);
      this.scope.remove = angular.bind(this, this.remove);

      this.scope.save = angular.bind(this, this.save);
      this.scope.saveAndList = angular.bind(this, this.saveAndList);
      this.scope.saveAndView = angular.bind(this, this.saveAndView);

      this.scope.listEnabled = angular.bind(this, this.listEnabled);
      this.scope.createEnabled = angular.bind(this, this.createEnabled);
      this.scope.viewEnabled = angular.bind(this, this.viewEnabled);
      this.scope.editEnabled = angular.bind(this, this.editEnabled);
      this.scope.removeEnabled = angular.bind(this, this.removeEnabled);
      this.scope.saveEnabled = angular.bind(this, this.saveEnabled);

      this.scope.createPermission = angular.bind(this, this.createPermission);
      this.scope.editPermission = angular.bind(this, this.editPermission);
      this.scope.removePermission = angular.bind(this, this.removePermission);
    }

    ListDetailController.prototype.load = function(promise) {
      var self = this;

      self.scope.loading = true;
      self.scope.items = [];

      return $q.when(promise).then(function(items) {
        self.scope.loading = false;
        self.scope.items = items;
      });
    };

    ListDetailController.prototype.discardChanges = function() {
      return $window.confirm('Discard unsaved changes?');
    };

    ListDetailController.prototype.list = function() {
      var ok = this.scope.item === null || !this.scope.editing || !this.scope.item.isDirty() ||
        this.discardChanges();

      if (!ok) {
        return;
      }

      this.scope.viewing = false;
      this.scope.editing = false;
      this.scope.originalItem = null;
      this.scope.item = null;
    };

    ListDetailController.prototype.view = function(item) {
      var ok = this.scope.item === null || !this.scope.editing || !this.scope.item.isDirty() ||
        this.discardChanges();

      if (!ok) {
        return;
      }

      this.scope.viewing = true;
      this.scope.editing = false;
      this.scope.originalItem = null;
      this.scope.item = item;
    };

    ListDetailController.prototype.edit = function(item) {
      var ok = this.scope.item === null || !this.scope.editing || !this.scope.item.isDirty() ||
        this.discardChanges();

      if (!ok) {
        return;
      }

      this.scope.viewing = false;
      this.scope.editing = true;
      this.scope.originalItem = item;
      this.scope.item = item.clone();
    };

    ListDetailController.prototype.remove = function(item) {
      var self = this;

      if (self.scope.item !== null && self.scope.item.getId() === item.getId()) {
        if (self.scope.item.isDirty() && !self.discardChanges()) {
          return;
        }

        self.scope.viewing = false;
        self.scope.editing = false;
        self.scope.originalItem = null;
        self.scope.item = null;
      }

      item.remove().then(function() {
        _.pull(self.scope.items, item);
      });
    };

    ListDetailController.prototype.save = function() {
      var self = this;

      self.scope.saving = true;

      return self.scope.item.save()
        .then(function(item) {
          var x = self.scope.items.indexOf(item);

          if (x === -1) {
            self.scope.items.push(item);
          }

          return item;
        })
        .finally(function() {
          self.scope.saving = false;
        });
    };

    ListDetailController.prototype.saveAndList = function() {
      var self = this;

      return self.save().then(function() {
        self.list();
      });
    };

    ListDetailController.prototype.saveAndView = function() {
      var self = this;

      return self.save().then(function(item) {
        self.view(item);
      });
    };

    ListDetailController.prototype.listEnabled = function() {
      return !this.scope.saving;
    };

    ListDetailController.prototype.createEnabled = function() {
      return !this.scope.saving;
    };

    ListDetailController.prototype.viewEnabled = function(item) {
      return item !== null &&
        item.getId() !== null &&
        !item.isDeleted &&
        !this.scope.saving;
    };

    ListDetailController.prototype.editEnabled = function(item) {
      return item !== null &&
        item.getId() !== null &&
        !item.isDeleted &&
        !this.scope.saving;
    };

    ListDetailController.prototype.removeEnabled = function(item) {
      return item !== null &&
        item.getId() !== null &&
        !item.isSaving &&
        !item.isDeleted;
    };

    ListDetailController.prototype.saveEnabled = function() {
      return !this.scope.saving;
    };

    ListDetailController.prototype.createPermission = function(item) {
      return this._createPermission.hasPermission();
    };

    ListDetailController.prototype.editPermission = function(item) {
      return this._editPermission.hasObjectPermission(item);
    };

    ListDetailController.prototype.removePermission = function(item) {
      return this._removePermission.hasObjectPermission(item);
    };

    return ListDetailController;
  });
})();
