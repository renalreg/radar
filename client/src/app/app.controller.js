(function() {
  'use strict';

  var app = angular.module('radar');

  app.controller('AppController', function(init, $rootScope) {
    $rootScope.init = false;

    init.then(function() {
      $rootScope.init = true;
    });
  });
})();
