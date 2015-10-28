(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudListAppendButton', function() {
    return {
      scope: {
        action: '&'
      },
      template: '<button type="button" class="btn btn-success" ng-click="action()">Add</button>'
    };
  });
})();
