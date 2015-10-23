(function() {
  'use strict';

  var app = angular.module('radar.notifications');

  app.directive('notifications', ['notificationService', function(notificationService) {
    return {
      scope: {},
      templateUrl: 'app/notifications/notifications.html',
      link: function(scope) {
        scope.notifications = notificationService.notifications;

        scope.getClass = function(notification) {
          return notification.type === 'success' ? 'alert-success' : 'alert-info';
        };
      }
    };
  }]);
})();
