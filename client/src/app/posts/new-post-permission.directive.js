(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.directive('newPostPermission', ['PostPermission', '$compile', function(PostPermission, $compile) {
    return {
      scope: true,
      link: function(scope, element, attrs) {
        var permission = new PostPermission();

        scope.$watch(function() {
          return permission.hasPermission();
        }, function(hasPermission) {
          scope.hasPermission = hasPermission;
        });

        // TODO this will overwrite an existing ng-if attribute
        element.attr('ng-if', 'hasPermission');
        element.removeAttr('new-post-permission');
        $compile(element)(scope);
      }
    };
  }]);
})();
