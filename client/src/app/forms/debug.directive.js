(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmDebug', function() {
    return {
      require: '^form',
      transclude: true,
      template: '<button ng-click="click()" type="button" ng-transclude></button>',
      link: function(scope, element, attrs, formCtrl) {
        scope.click = function() {
          console.log(formCtrl);
        };
      }
    };
  });
})();

