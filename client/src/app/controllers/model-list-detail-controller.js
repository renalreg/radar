(function() {
  'use strict';

  var app = angular.module('radar.controllers');

  function factory(
    _,
    $window,
    $q,
    GrantPermission
  ) {
    /** Controller for managing a list of models */
    function ModelListDetailController($scope, params) {
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
      this.scope.cancelEnabled = angular.bind(this, this.cancelEnabled);

      this.scope.createPermission = angular.bind(this, this.createPermission);
      this.scope.editPermission = angular.bind(this, this.editPermission);
      this.scope.removePermission = angular.bind(this, this.removePermission);

      this.scope.createVisible = angular.bind(this, this.createVisible);
      this.scope.editVisible = angular.bind(this, this.editVisible);
      this.scope.removeVisible = angular.bind(this, this.removeVisible);
    }

    ModelListDetailController.$inject = ['$scope', 'params'];

    ModelListDetailController.prototype.load = function(promise) {
      var self = this;

      self.scope.loading = true;
      self.scope.items = [];

      return $q.when(promise).then(function(items) {
        self.scope.loading = false;
        self.scope.items = items;
      });
    };

    ModelListDetailController.prototype.discardChanges = function() {
      return $window.confirm('Discard unsaved changes?');
    };

    ModelListDetailController.prototype.list = function() {
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

    ModelListDetailController.prototype.view = function(item) {
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

    ModelListDetailController.prototype.edit = function(item) {
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

    ModelListDetailController.prototype.remove = function(item) {
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

      return item.remove().then(function() {
        _.pull(self.scope.items, item);
      });
    };

    ModelListDetailController.prototype.save = function() {
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
        ['finally'](function() {
          self.scope.saving = false;
        });
    };

    ModelListDetailController.prototype.saveAndList = function() {
      var self = this;

      return self.save().then(function() {
        self.list();
      });
    };

    ModelListDetailController.prototype.saveAndView = function() {
      var self = this;

      return self.save().then(function(item) {
        self.view(item);
      });
    };

    ModelListDetailController.prototype.listEnabled = function() {
      return !this.scope.saving;
    };

    ModelListDetailController.prototype.createEnabled = function() {
      return !this.scope.saving;
    };

    ModelListDetailController.prototype.viewEnabled = function(item) {
      return item !== null &&
        item.getId() !== null &&
        !item.isDeleted &&
        !this.scope.saving;
    };

    ModelListDetailController.prototype.editEnabled = function(item) {
      return item !== null &&
        item.getId() !== null &&
        !item.isDeleted &&
        !this.scope.saving;
    };

    ModelListDetailController.prototype.removeEnabled = function(item) {
      return item !== null &&
        item.getId() !== null &&
        !item.isSaving &&
        !item.isDeleted;
    };

    ModelListDetailController.prototype.saveEnabled = function() {
      return !this.scope.saving;
    };

    ModelListDetailController.prototype.cancelEnabled = function() {
      return !this.scope.saving;
    };

    ModelListDetailController.prototype.createPermission = function() {
      return this._createPermission.hasPermission();
    };

    ModelListDetailController.prototype.editPermission = function(item) {
      return this._editPermission.hasObjectPermission(item);
    };

    ModelListDetailController.prototype.removePermission = function(item) {
      return this._removePermission.hasObjectPermission(item);
    };

    ModelListDetailController.prototype.createVisible = function() {
      return true;
    };

    ModelListDetailController.prototype.editVisible = function(item) {
      return item !== null && item.getId() !== null;
    };

    ModelListDetailController.prototype.removeVisible = function(item) {
      return item !== null && item.getId() !== null;
    };

    return ModelListDetailController;
  }

  factory.$inject = [
    '_',
    '$window',
    '$q',
    'GrantPermission'
  ];

  app.factory('ModelListDetailController', factory);
})();
