(function() {
  'use strict';

  var app = angular.module('radar.notifications');

  var TYPE_TO_CLASS = {
    success: 'alert-success',
    fail: 'alert-danger',
    info: 'alert-info'
  };

  app.directive('notifications', ['notificationService', function(notificationService) {
    return {
      scope: {},
      templateUrl: 'app/notifications/notifications.html',
      link: function(scope) {
        scope.notifications = notificationService.notifications;

        scope.getClass = function(notification) {
          return TYPE_TO_CLASS[notification.type] || 'alert-info';
        };
      }
    };
  }]);
})();
