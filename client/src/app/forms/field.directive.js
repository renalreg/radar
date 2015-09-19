(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmField', function(_) {
    function Field($scope, $attrs) {
      this.scope = $scope;
      this.attrs = $attrs;
      this.valid = true;
      this.required = false;
      this.labels = 0;
      this.modelCtrl = null;
    }

    Field.prototype.setValid = function(valid) {
      this.valid = valid;
    };

    Field.prototype.setModelCtrl = function(modelCtrl) {
      this.modelCtrl = modelCtrl;
    };

    Field.prototype.setRequired = function(required) {
      this.required = required;
    };

    Field.prototype.registerLabel = function() {
      this.labels += 1;
    };

    Field.prototype.isValid = function() {
      return this.valid && (this.modelCtrl === null || this.modelCtrl.$pristine || this.modelCtrl.$valid);
    };

    Field.prototype.isRequired = function() {
      return this.required;
    };

    Field.prototype.hasLabel = function() {
      return this.labels > 0;
    };

    return {
      controller: Field
    };
  });
})();
