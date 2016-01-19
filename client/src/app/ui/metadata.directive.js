(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('metadata', function() {
    return {
      scope: {
        item: '='
      },
      templateUrl: 'app/ui/metadata.html'
    };
  });
})();
