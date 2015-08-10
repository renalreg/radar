(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.factory('DetailService', function(humps) {
    function DetailService() {
      this.item = null;
      this.isViewing = false;
      this.isEditing = false;
      this.isSaving = false;
      this.errors = {};
    }

    DetailService.prototype.view = function(item) {
      this.item = item;
      this.isViewing = true;
      this.isEditing = false;
      this.isSaving = false;
      this.errors = {};
    };

    DetailService.prototype.edit = function(item) {
      this._item = item;
      this.item = angular.copy(item);
      this.isViewing = false;
      this.isEditing = true;
      this.isSaving = false;
      this.errors = {};
    };

    DetailService.prototype.isModified = function() {
      return angular.equals(this._item, this.item);
    };

    DetailService.prototype.save = function() {
      var self = this;

      self.isSaving = true;

      return this.item.$save().then(function(item) {
        self.isSaving = false;
        angular.copy(item, self._item);
        self._item.hello = 'hello';
        return self._item;
      }, function(response) {
        self.isSaving = false;

        if (response.status === 422) {
          self.errors = humps.camelizeKeys(response.data.errors);
        }
      });
    };

    DetailService.prototype.cancel = function() {
      this.item = null;
      this.isViewing = false;
      this.isEditing = false;
      this.isSaving = false;
    };

    return DetailService;
  });
})();
