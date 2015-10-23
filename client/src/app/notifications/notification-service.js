(function() {
  'use strict';

  var app = angular.module('radar.notifications');

  app.factory('notificationService', ['$timeout', function($timeout) {
    var notifications = [];

    return {
      notifications: notifications,
      success: success,
      remove: remove
    };

    function success(params) {
      if (!angular.isObject(params)) {
        params = {message: params};
      }

      if (params['title'] === undefined) {
        params['title'] = 'Success!';
      }

      params['type'] = 'success';

      return _notify(params);
    }

    function _notify(params) {
      if (params['timeout'] === undefined) {
        params['timeout'] = 5000; // 5 seconds
      }

      var notification = {
        type: params['type'],
        title: params['title'],
        message: params['message'],
        timeout: params['timeout'],
        remove: function() {
          remove(this);
        }
      };

      if (notification['timeout'] > 0) {
        $timeout(function() {
          remove(notification)
        }, notification['timeout']);
      }

      notifications.push(notification);

      return notification;
    }

    function remove(notification) {
      _.pull(notifications, notification);
    }
  }]);
})();
