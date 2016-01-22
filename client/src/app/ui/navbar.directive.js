(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('navbar', ['session', 'hasPermission', function(session, hasPermission) {
    return {
      restrict: 'A',
      scope: true,
      templateUrl: 'app/ui/navbar.html',
      link: function(scope) {
        scope.$watch(function() {
          return session.user;
        }, function(user) {
          scope.showPatients = hasPermission(user, 'VIEW_PATIENT');
          scope.showUsers = hasPermission(user, 'VIEW_USER');
        });
      }
    };
  }]);
})();
