(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('paginationHelper', function() {
    var LEFT_EDGE = 2;
    var RIGHT_EDGE = 2;
    var LEFT_CURRENT = 2;
    var RIGHT_CURRENT = 5;

    return {
      require: '^listHelper',
      scope: {},
      templateUrl: 'app/ui/pagination-helper.html',
      link: function(scope, element, attrs, listHelperCtrl) {
        var leftEdge = 2;
        var rightEdge = 2;
        var leftCurrent = 2;
        var rightCurrent = 5;

        scope.getPage = getPage;
        scope.setPage = setPage;
        scope.getPerPage = getPerPage;
        scope.setPerPage = setPerPage;
        scope.getTotalPages = getTotalPages;
        scope.hasPrevious = hasPrevious;
        scope.hasNext = hasNext;
        scope.previousPage = previousPage;
        scope.nextPage = nextPage;
        scope.firstPage = firstPage;
        scope.lastPage = lastPage;
        scope.isCurrentPage = isCurrentPage;
        scope.isJump = isJump;

        scope.page = listHelperCtrl.getPage();
        scope.perPage = listHelperCtrl.getPerPage();

        scope.$watch('page', function(value) {
          setPage(value);
        });

        scope.$watch(function() {
          return getPage();
        }, function(value) {
          scope.page = value;
          scope.pages = getPages();
        });

        scope.$watch('perPage', function(value) {
          setPerPage(value);
        });

        scope.$watch(function() {
          return getPerPage();
        }, function(value) {
          scope.perPage = value;
        });

        scope.$watch(function() {
          return getTotalPages();
        }, function() {
          scope.pages = getPages();
        });

        function getPage() {
          return listHelperCtrl.getPage();
        }

        function setPage(page) {
          listHelperCtrl.setPage(page);
        }

        function getPerPage() {
          return listHelperCtrl.getPerPage();
        }

        function setPerPage(perPage) {
          listHelperCtrl.setPerPage(perPage);
        }

        function getTotalPages() {
          return listHelperCtrl.getTotalPages();
        }

        function hasPrevious() {
          return getPage() > 1;
        }

        function hasNext() {
          return getPage() < getTotalPages();
        }

        function previousPage() {
          setPage(getPage() - 1);
        }

        function nextPage() {
          setPage(getPage() + 1);
        }

        function firstPage() {
          setPage(1);
        }

        function lastPage() {
          setPage(getTotalPages());
        }

        function getPages() {
          var page = getPage();
          var totalPages = getTotalPages();
          var pages = [];
          var last = 0;

          for (var i = 1; i <= totalPages; i++) {
            if (
              i <= LEFT_EDGE ||
              (
                i > page - LEFT_CURRENT &&
                i < page + RIGHT_CURRENT
              ) ||
              i > totalPages - RIGHT_EDGE
            ) {
              if (last + 1 != i) {
                pages.push(null);
              }

              pages.push(i);
              last = i;
            }
          }

          return pages;
        }

        function isCurrentPage(page) {
          return page === getPage();
        }

        function isJump(page) {
          return page === null;
        }
      }
    };
  });
})();
