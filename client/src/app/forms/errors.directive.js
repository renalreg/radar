(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmErrors', function(_) {
    return {
      require: ['frmErrors', '^frmField'],
      templateUrl: 'app/forms/errors.html',
      transclude: true,
      scope: {
        errors: '='
      },
      link: function(scope, element, attrs, ctrls) {
        var errorsCtrl = ctrls[0];
        var fieldCtrl = ctrls[1];

        scope.$watch(function() {
          return fieldCtrl.modelCtrl;
        }, function (value) {
          if (value) {
            errorsCtrl.modelCtrl = value;
          } else {
            errorsCtrl.modelCtrl = null;
          }
        });

        scope.$watch('errors', function(errors) {
          fieldCtrl.setValid(_.keys(errors).length === 0);
          scope.errors = errors;
        });
      },
      controller: function() {
        this.overrides = {};
        this.modelCtrl = null;

        this.showError = function(key, isDefault) {
          return this.modelCtrl !== null && this.modelCtrl.$error[key] && this.modelCtrl.$dirty && (!isDefault || !this.overrides[key]);
        };

        this.override = function(key) {
          this.overrides[key] = true;
        };
      }
    };
  });
})();
