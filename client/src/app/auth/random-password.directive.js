(function() {
  'use strict';

  var app = angular.module('radar.auth');

  app.directive('randomPassword', ['randomPassword', function(randomPassword) {
    return {
      restrict: 'A',
      require: 'ngModel',
      scope: true,
      templateUrl: 'app/auth/random-password.html',
      link: function(scope, element, attrs, ngModel) {
        scope.loading = false;

        scope.generate = function() {
          scope.loading = true;

          randomPassword()
            .then(function(password) {
              scope.password = password;
              ngModel.$setViewValue(password);
            })
            ['finally'](function() {
              scope.loading = false;
            });
        };
      }
    };
  }]);
})();
