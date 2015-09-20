(function() {
  'use strict';

  var app = angular.module('radar.account.changePassword');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('changePassword', {
      url: '/change-password',
      templateUrl: 'app/account/change-password/change-password.html'
    });
  }]);
})();
