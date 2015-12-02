(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudSubmit', ['$parse', function($parse) {
    return {
      require: ['form', 'crudSubmit'],
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
        var crudSubmitCtrl = ctrls[1];

        element.on('submit', function(event) {
          event.preventDefault();

          scope.$apply(function() {
            var promise = $parse(attrs.crudSubmit)(scope);

            crudSubmitCtrl.broadcast('submit');

            promise
              .then(function() {
                formCtrl.$setPristine(true);
              })
              ['finally'](function() {
                crudSubmitCtrl.broadcast('submitted');
              });
          });
        });
      }
    };
  }]);
})();
