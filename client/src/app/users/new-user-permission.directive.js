(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.directive('newUserPermission', ['hasEditUserMembershipPermission', '$compile', 'session', function(hasEditUserMembershipPermission, $compile, session) {
    return {
      scope: true,
      link: function(scope, element, attrs) {
        scope.$watch(function() {
          return hasEditUserMembershipPermission(session.user);
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
