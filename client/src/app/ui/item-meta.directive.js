(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('itemMeta', function() {
    return {
      scope: {
        item: '='
      },
      templateUrl: 'app/ui/item-meta.html'
    };
  });
})();
