(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('sortHelper', function() {
    return {
      require: '^listHelper',
      scope: {},
      transclude: true,
      templateUrl: 'app/ui/sort-helper.html',
      link: function(scope, element, attrs, listHelperCtrl) {
        scope.sort = function() {
          var sortBy = getSortBy();
          var reverse = getReverse();

          if (isSorted()) {
            var currentReverse = listHelperCtrl.getReverse();
            listHelperCtrl.sort(sortBy, !currentReverse);
          } else {
            listHelperCtrl.sort(sortBy, reverse);
          }
        };

        scope.isAscending = isAscending;
        scope.isDescending = isDescending;

        function isAscending() {
          return isSorted() && !listHelperCtrl.getReverse();
        }

        function isDescending() {
          return isSorted() && listHelperCtrl.getReverse();
        }

        function isSorted() {
          var sortBy = getSortBy();
          var currentSortBy = listHelperCtrl.getSortBy();
          return sortBy === currentSortBy;
        }

        function getSortBy() {
          return attrs.sortHelper;
        }

        function getReverse() {
          return attrs.reverse === 'true';
        }
      }
    };
  });
})();
