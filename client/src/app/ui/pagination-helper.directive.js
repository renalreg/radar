(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('paginationHelper', function() {
    // TODO allow updating page and perPage from template

    return {
      require: '^listHelper',
      scope: {},
      templateUrl: 'app/ui/pagination-helper.html',
      link: function(scope, element, attrs, listHelperCtrl) {
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

          for (var i = 1; i <= totalPages; i++) {
            pages.push({
              number: i,
              active: i === page
            });
          }

          return pages;
        }

        scope.$watch(function() {
          return getPage();
        }, function() {
          scope.pages = getPages();
        });

        scope.$watch(function() {
          return getTotalPages();
        }, function() {
          scope.pages = getPages();
        });
      }
    };
  });
})();
