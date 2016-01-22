(function() {
  'use strict';

  var app = angular.module('radar.ui.fatalError');

  app.directive('fatalError', ['$window', 'notificationService', '_', function($window, notificationService, _) {
    return {
      templateUrl: 'app/ui/fatal-error/fatal-error.html',
      link: function(scope) {
        scope.notification = null;

        scope.reload = function() {
          $window.location.reload();
        };

        scope.close = function() {
          scope.notification.remove();
        };

        scope.$watchCollection(function() {
          return notificationService.notifications;
        }, function(notifications) {
          scope.notification = _.find(notifications, function(notification) {
            return notification.type === 'fatal';
          });
        });
      }
    };
  }]);
})();
