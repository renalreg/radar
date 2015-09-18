(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('AppController', function(boot, $rootScope) {
    $rootScope.ready = false;

    boot.then(function() {
      $rootScope.ready = true;
    });
  });
})();
