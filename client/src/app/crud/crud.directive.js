(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crud', function() {
    return {
      controller: function ($scope) {
        this.list = function() {
          return $scope.list.apply(this, arguments);
        };

        this.view = function() {
          return $scope.view.apply(this, arguments);
        };

        this.edit = function() {
          return $scope.edit.apply(this, arguments);
        };

        this.remove = function() {
          return $scope.remove.apply(this, arguments);
        };

        this.save = function() {
          return $scope.save.apply(this, arguments);
        };

        this.saveAndList = function() {
          return $scope.saveAndList.apply(this, arguments);
        };

        this.saveAndView = function() {
          return $scope.saveAndView.apply(this, arguments);
        };

        this.listEnabled = function() {
          return $scope.listEnabled.apply(this, arguments);
        };

        this.createEnabled = function() {
          return $scope.createEnabled.apply(this, arguments);
        };

        this.viewEnabled = function() {
          return $scope.viewEnabled.apply(this, arguments);
        };

        this.editEnabled = function() {
          return $scope.editEnabled.apply(this, arguments);
        };

        this.removeEnabled = function() {
          return $scope.removeEnabled.apply(this, arguments);
        };

        this.saveEnabled = function() {
          return $scope.saveEnabled.apply(this, arguments);
        };

        this.cancelEnabled = function() {
          return $scope.cancelEnabled.apply(this, arguments);
        };

        this.createPermission = function() {
          return $scope.createPermission.apply(this, arguments);
        };

        this.editPermission = function() {
          return $scope.editPermission.apply(this, arguments);
        };

        this.removePermission = function() {
          return $scope.removePermission.apply(this, arguments);
        };
      }
    };
  });
})();

