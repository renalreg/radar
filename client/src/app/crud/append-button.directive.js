(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudAppendButton', function() {
    return {
      scope: {
        action: '&'
      },
      template: '<button type="button" class="btn btn-success" ng-click="action()">Add</button>'
    };
  });
})();
