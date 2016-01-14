(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudSubmit', ['$parse', function($parse) {
    return {
      require: ['form', 'crudSubmit'],
      controller: ['$scope', '$attrs', function($scope, $attrs) {
        var listeners = {};

        this.on = on;
        this.broadcast = broadcast;
        this.submit = submit;

        function on(name, callback) {
          if (listeners[name] === undefined) {
            listeners[name] = [];
          }

          var callbacks = listeners[name];
          callbacks.push(callback);
        }

        function broadcast(name) {
          var callbacks = listeners[name] || [];
          var args = Array.prototype.slice.call(arguments, 1);

          for (var i = 0; i < callbacks.length; i++) {
            var callback = callbacks[i];
            callback.apply(this, args);
          }
        }

        function submit(action) {
          var promise;

          broadcast('submitting', true);

          if (action) {
            promise = action();
          } else {
            promise = $parse($attrs.crudSubmit)($scope);
          }

          promise
            .then(function() {
              broadcast('success');
            })
            ['catch'](function() {
              broadcast('failure');
            })
            ['finally'](function() {
              broadcast('submitting', false);
            });
        }
      }],
      link: function(scope, element, attrs, ctrls) {
        var formCtrl = ctrls[0];
        var crudSubmitCtrl = ctrls[1];

        element.on('submit', function(event) {
          scope.$apply(function() {
            crudSubmitCtrl.submit();
          });
        });

        crudSubmitCtrl.on('success', function() {
          console.log('pristine!');
          formCtrl.$setPristine(true);
        });
      }
    };
  }]);
})();
