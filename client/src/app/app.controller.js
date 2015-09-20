(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('AppController', ['boot', '$rootScope', function(boot, $rootScope) {
    $rootScope.ready = false;

    boot.then(function() {
      $rootScope.ready = true;
    });
  }]);
})();
