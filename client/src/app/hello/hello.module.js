(function() {
  'use strict';

  var app = angular.module('radar.hello', ['ui.router']);

  app.factory('FooController', function(DetailController) {
    function FooController($scope, $injector, store) {
      var self = this;

      $injector.invoke(DetailController, self, {$scope: $scope});

      self.load(store.findOne('dialysis', 1296)).then(function() {
        self.view();
      });
    }

    FooController.prototype = Object.create(DetailController.prototype);

    return FooController;
  });

  app.directive('fooComponent', function(FooController) {
    return {
      scope: {
        patient: '='
      },
      controller: FooController,
      templateUrl: 'app/hello/foo-component.html'
    };
  });

  app.directive('paginationHelper', function() {
    // TODO allow updating page and perPage from template

    return {
      require: '^listHelper',
      scope: {},
      templateUrl: 'app/hello/pagination-helper.html',
      link: function(scope, element, attrs, listHelperCtrl) {
        scope.page = listHelperCtrl.page;
        scope.perPage = listHelperCtrl.perPage;
        scope.total = 0;
        scope.totalPages = 0;
        scope.pages = [];

        scope.setPage = setPage;
        scope.hasPrevious = hasPrevious;
        scope.hasNext = hasNext;

        scope.$watchCollection(function() {
          return listHelperCtrl.sortedItems;
        }, function() {
          updateTotal();
          updateTotalPages();
          updatePages();
        });

        scope.$watch(function() {
          return listHelperCtrl.page;
        }, function(page) {
          setPage(page);
          updatePages();
        });

        scope.$watch(function() {
          return listHelperCtrl.page;
        }, function(page) {
          setPage(page);
          updatePages();
        });

        scope.$watch(function() {
          return listHelperCtrl.perPage;
        }, function(perPage) {
          scope.perPage = perPage;
          updateTotalPages();
        });

        function setPage(page) {
          if (page > 0 && page <= scope.totalPages) {
            scope.page = page;
            listHelperCtrl.page = scope.page;
            updatePages();
          }
        }

        function hasPrevious() {
          return scope.page > 1;
        }

        function hasNext() {
          return scope.page < scope.totalPages;
        }

        function updateTotal() {
          scope.total = listHelperCtrl.sortedItems.length;
          updateTotalPages();
        }

        function updateTotalPages() {
          scope.totalPages = Math.ceil(scope.total / scope.perPage);

          if (scope.page > scope.totalPages) {
            if (scope.totalPages === 0) {
              scope.page = 1;
            } else {
              scope.page = scope.totalPages;
            }

            listHelperCtrl.page = scope.page;
          }

          updatePages();
        }

        function updatePages() {
          var pages = [];

          for (var i = 1; i <= scope.totalPages; i++) {
            var page = {
              number: i,
              active: i === scope.page
            };
            pages.push(page);
          }

          scope.pages = pages;
        }
      }
    };
  });

  app.directive('sortHelper', function() {
    // TODO show direction icon

    return {
      require: '^listHelper',
      scope: {},
      transclude: true,
      templateUrl: 'app/hello/sort-helper.html',
      link: function(scope, element, attrs, listHelperCtrl) {
        scope.sort = function() {
          var sortBy = attrs.sortHelper;
          var reverse = attrs.reverse === 'true';

          if (listHelperCtrl.sortBy === sortBy) {
            listHelperCtrl.reverse = !listHelperCtrl.reverse;
          } else {
            listHelperCtrl.sortBy = sortBy;
            listHelperCtrl.reverse = reverse;
          }
        };
      }
    };
  });

  app.directive('filterHelper', function() {
    return {
      require: '^listHelper',
      scope: {},
      templateUrl: 'app/hello/filter-helper.html',
      link: function(scope, element, attrs, listHelperCtrl) {
        scope.listHelperCtrl = listHelperCtrl;

        scope.clear = function() {
          scope.listHelperCtrl.search = '';
        };
      }
    };
  });

  app.directive('listHelper', function($parse, _, $filter) {
    // TODO support server-side pagination
    // TODO check perPage is in range

    return {
      scope: true,
      controller: function($scope, $attrs) {
        var self = this;

        var collectionGetter = angular.noop;

        self.items = [];
        self.filteredItems = [];
        self.sortedItems = [];
        self.paginatedItems = [];
        self.page = 1;
        self.perPage = 10;
        self.sortBy = null;
        self.reverse = false;
        self.search = '';

        $attrs.$observe('perPage', function(value) {
          // TODO convert to int
          self.perPage = value;
        });

        $attrs.$observe('listHelper', function(value) {
          var match = /\s*(\S+)\s+as\s+(\S+)\s*/.exec(value);

          if (match) {
            var collectionExpression = match[1];
            var aliasExpression = match[2];

            collectionGetter = $parse(collectionExpression);
            var aliasSetter = $parse(aliasExpression).assign;

            self.items = collectionGetter($scope);
            aliasSetter($scope, self);
          } else {
            throw 'Expected "x as y" but got: ' + value;
          }
        });

        $scope.$watchCollection(function() {
          return collectionGetter($scope) || [];
        }, function(newItems) {
          self.items = newItems;
        });

        // objectEquality = true so we re-filter when any of the objects change
        $scope.$watch(function() {
          return self.items;
        }, function() {
          filter();
        }, true);

        $scope.$watch(function() {
          return self.search;
        }, function() {
          self.page = 1;
          filter();
        });

        $scope.$watch(function() {
          return self.sortBy;
        }, function() {
          self.page = 1;
          sort();
        });

        $scope.$watch(function() {
          return self.reverse;
        }, function() {
          self.page = 1;
          sort();
        });

        $scope.$watch(function() {
          return self.page;
        }, function() {
          paginate();
        });

        $scope.$watch(function() {
          return self.perPage;
        }, function() {
          self.page = 1;
          paginate();
        });

        function filter() {
          var filteredItems = self.items;

          if (self.search) {
            filteredItems = $filter('filter')(filteredItems, self.search);
          }

          self.filteredItems = filteredItems;

          sort();
        }

        function sort() {
          var sortedItems = self.filteredItems;

          if (self.sortBy !== null) {
            var getter = $parse(self.sortBy);
            sortedItems = _.sortBy(self.filteredItems, function(item) {
              return getter(item);
            });
          }

          if (self.reverse) {
            sortedItems.reverse();
          }

          self.sortedItems = sortedItems;

          paginate();
        }

        function paginate() {
          var startIndex = (self.page - 1) * self.perPage;
          var endIndex = self.page * self.perPage;
          self.paginatedItems = _.slice(self.sortedItems, startIndex, endIndex);
        }
      }
    };
  });
})();
