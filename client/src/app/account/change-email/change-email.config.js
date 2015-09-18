(function() {
  'use strict';

  var app = angular.module('radar.account.changeEmail');

  app.config(function($stateProvider) {
    $stateProvider.state('changeEmail', {
      url: '/change-email',
      templateUrl: 'app/account/change-email/change-email.html'
    });
  });
})();
