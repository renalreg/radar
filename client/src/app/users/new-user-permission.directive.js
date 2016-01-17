(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.directive('newUserPermission', ['hasPermission', '$compile', 'session', function(hasPermission, $compile, session) {
    return {
      scope: true,
      link: function(scope, element, attrs) {
        scope.$watch(function() {
          return hasPermission(session.user, 'EDIT_USER_MEMBERSHIP');
        }, function(hasPermission) {
          scope.hasPermission = hasPermission;
        });

        // TODO this will overwrite an existing ng-if attribute
        element.attr('ng-if', 'hasPermission');
        element.removeAttr('new-user-permission');
        $compile(element)(scope);
      }
    };
  }]);
})();
