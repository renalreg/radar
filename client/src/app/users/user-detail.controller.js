(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.controller('UserDetailController', function($scope, user) {
    $scope.user = user;
  });
})();
