(function() {
  'use strict';

  var app = angular.module('radar.notifications');

  app.factory('notificationService', ['$timeout', '_', function($timeout, _) {
    var notifications = [];

    return {
      notifications: notifications,
      success: success,
      fail: fail,
      info: info,
      remove: remove
    };

    function toParams(params) {
      if (angular.isArray(params) || !angular.isObject(params)) {
        params = {message: params};
      }

      return params
    }

    function setDefaults(params, defaults) {
      _.each(defaults, function(value, key) {
        if (params[key] === undefined) {
          params[key] = value;
        }
      });
    }

    function success(params) {
      params = toParams(params);
      setDefaults(params, {
        title: 'Success',
        icon: 'fa-check-circle',
        type: 'success'
      });
      return _notify(params);
    }

    function fail(params) {
      params = toParams(params);
      setDefaults(params, {
        title: 'Error',
        icon: 'fa-exclamation-circle',
        type: 'fail'
      });
      return _notify(params);
    }

    function info(params) {
      params = toParams(params);
      setDefaults(params, {
        title: 'Info',
        icon: 'fa-info-circle',
        type: 'info'
      });
      return _notify(params);
    }

    function _notify(params) {
      if (angular.isArray(params.message)) {
        params.message = params.message.join(' ');
      }

      if (params.timeout === undefined) {
        params.timeout = 5000; // 5 seconds
      }

      var notification = {
        type: params.type,
        title: params.title,
        message: params.message,
        icon: params.icon,
        timeout: params.timeout,
        remove: function() {
          remove(this);
        }
      };

      if (notification.timeout > 0) {
        $timeout(function() {
          remove(notification);
        }, notification.timeout);
      }

      notifications.push(notification);

      return notification;
    }

    function remove(notification) {
      _.pull(notifications, notification);
    }
  }]);
})();
