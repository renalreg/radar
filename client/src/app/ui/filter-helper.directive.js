(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('filterHelper', function() {
    return {
      require: '^listHelper',
      scope: {},
      templateUrl: 'app/ui/filter-helper.html',
      link: function(scope, element, attrs, listHelperCtrl) {
        scope.search = '';

        scope.$watch('search', function(value) {
          listHelperCtrl.filter(value);
        });

        scope.clear = function() {
          scope.search = '';
          listHelperCtrl.filter('');
        };
      }
    };
  });
})();
