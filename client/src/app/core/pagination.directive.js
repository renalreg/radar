(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.directive('rrPagination', function() {
    return {
      restrict: 'A',
      templateUrl: 'app/core/pagination.html',
      scope: {
        page: '=',
        total: '='
      },
      link: function(scope) {
        scope.hasPrevious = hasPrevious;
        scope.hasNext = hasNext;
        scope.setPage = setPage;

        scope.totalPages = getTotalPages();
        scope.pages = getPages();

        scope.$watch('page', function() {
          scope.pages = getPages();
        });

        scope.$watch('total', function() {
          scope.totalPages = getTotalPages();

          if (scope.page > scope.totalPages) {
            setPage(scope.totalPages);
          }

          scope.pages = getPages();
        });

        function hasPrevious() {
          return scope.page > 1;
        }

        function hasNext() {
          return scope.page < scope.totalPages;
        }

        function setPage(page) {
          if (page > 0 && page < scope.totalPages) {
            scope.page = page;
          }
        }

        function getPages() {
          var pages = [];

          for (var i = 1; i <= scope.totalPages; i++) {
            var page = {
              number: i,
              active: i === scope.page
            };
            pages.push(page);
          }

          return pages;
        }

        function getTotalPages() {
          // TODO make items per page configurable
          return Math.ceil(scope.total / 3);
        }
      }
    };
  });
})();
