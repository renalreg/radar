(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('submitIfValid', function() {
    return {
      require: ['^form', 'submitIfValid'],
      scope: {
        submit: '&submitIfValid'
      },
      controller: function() {
        var listeners = {};

        this.on = on;
        this.broadcast = broadcast;

        function on(name, callback) {
          if (listeners[name] === undefined) {
            listeners[name] = [];
          }

          var callbacks = listeners[name];
          callbacks.push(callback);
        }

        function broadcast(name) {
          var callbacks = listeners[name] || [];

          for (var i = 0; i < callbacks.length; i++) {
            var callback = callbacks[i];
            callback(name);
          }
        }
      },
      link: function(scope, element, attrs, ctrls) {
        var formCtrl = ctrls[0];
        var submitIfValidCtrl = ctrls[1];

        element.on('submit', function(event) {
          event.preventDefault();

          if (formCtrl.$valid) {
            submitIfValidCtrl.broadcast('submit');

            scope.submit()['finally'](function() {
              submitIfValidCtrl.broadcast('submitted');
            });
          }
        });
      }
    };
  });
})();
