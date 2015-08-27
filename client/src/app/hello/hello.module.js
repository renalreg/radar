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

          var currentSortBy = listHelperCtrl.getSortBy();
          var currentReverse = listHelperCtrl.getReverse();

          if (currentSortBy === sortBy) {
            listHelperCtrl.sort(sortBy, !currentReverse);
          } else {
            listHelperCtrl.sort(sortBy, reverse);
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
        scope.search = '';

        scope.$watch('search', function(value) {
          console.log(value);
          listHelperCtrl.filter(value);
        });

        scope.clear = function() {
          listHelperCtrl.filter('');
        };
      }
    };
  });

  app.directive('listHelper', function($parse, _, $filter) {
    return {
      scope: false,
      controller: function($scope, $attrs) {
        var self = this;

        var listHelper = $attrs.listHelper;
        var match = /\s*(\S+)\s+as\s+(\S+)\s*/.exec(listHelper);

        if (match) {
          var collectionExpression = match[1];
          var aliasExpression = match[2];

          var collectionGetter = $parse(collectionExpression);
          var aliasSetter = $parse(aliasExpression).assign;

          client(collectionGetter, aliasSetter);
        } else {
          var paramsGetter = $parse(listHelper);
          server(paramsGetter);
        }

        function client(collectionGetter, aliasSetter) {
          aliasSetter($scope, self);

          var items = [];
          var filteredItems = [];
          var sortedItems = [];
          var paginatedItems = [];

          var sortBy = 'id';
          var reverse = false;

          var page = 1;
          var perPage = 10;

          var search = '';

          $scope.$watchCollection(function() {
            return collectionGetter($scope) || [];
          }, function(value) {
            items = value;
            _filter();
          });

          $attrs.$observe('perPage', function(value) {
            if (value) {
              perPage = parseInt(value);
              _paginate();
            }
          });

          $scope.$watch(function() {
            return items;
          }, function() {
            _filter();
          }, true);

          _filter();

          self.sort = sort;
          self.filter = filter;
          self.getSortBy = getSortBy;
          self.getReverse = getReverse;
          self.getPage = getPage;
          self.setPage = setPage;
          self.getPerPage = getPerPage;
          self.setPerPage = setPerPage;
          self.getTotalPages = getTotalPages;
          self.getCount = getCount;
          self.getItems = getItems;

          function sort(newSortBy, newReverse) {
            sortBy = newSortBy;
            reverse = newReverse;
            page = 1;
            _sort();
          }

          function filter(newSearch) {
            search = newSearch;
            _filter();
          }

          function getSortBy() {
            return sortBy;
          }

          function getReverse() {
            return reverse;
          }

          function getPage() {
            return page;
          }

          function setPage(newPage) {
            page = newPage;
            _paginate();
          }

          function getPerPage() {
            return perPage;
          }

          function setPerPage(newPerPage) {
            perPage = newPerPage;
            _paginate();
          }

          function getTotalPages() {
            return Math.ceil(filteredItems.length / perPage);
          }

          function getCount() {
            return filteredItems.length;
          }

          function getItems() {
            return paginatedItems;
          }

          function _filter() {
            filteredItems = items;

            if (search) {
              // TODO handle searching for dates better
              filteredItems = $filter('filter')(filteredItems, search);
            }

            _sort();
          }

          function _sort() {
            sortedItems = filteredItems;

            if (sortBy !== null) {
              var getter = $parse(sortBy);
              sortedItems = _.sortBy(sortedItems, function(item) {
                return getter(item);
              });
            }

            if (reverse) {
              sortedItems.reverse();
            }

            _paginate();
          }

          function _paginate() {
            var startIndex = (page - 1) * perPage;
            var endIndex = page * perPage;
            paginatedItems = _.slice(sortedItems, startIndex, endIndex);
          }
        }

        function server(apiGetter) {
          var api;

          $scope.$watch(function() {
            return apiGetter($scope);
          }, function(value) {
            api = value;
          });

          self.sort = sort;
          self.getSortBy = getSortBy;
          self.getReverse = getReverse;
          self.getPage = getPage;
          self.setPage = setPage;
          self.getPerPage = getPerPage;
          self.setPerPage = setPerPage;
          self.getTotalPages = getTotalPages;
          self.getCount = getCount;
          self.getItems = getItems;

          function sort(sortBy, reverse) {
            api.sort(sortBy, reverse);
          }

          function getSortBy() {
            return api.getSortBy();
          }

          function getReverse() {
            return api.getReverse();
          }

          function getPage() {
            return api.getPage();
          }

          function setPage(page) {
            api.setPage(page);
          }

          function getPerPage() {
            return api.getPerPage();
          }

          function setPerPage(perPage) {
            api.setPerPage(perPage);
          }

          function getTotalPages() {
            return api.getTotalPages();
          }

          function getCount() {
            return api.getCount();
          }

          function getItems() {
            return api.getItems();
          }
        }
      }
    };
  });

  app.factory('ListHelperProxy', function() {
    function ListHelperProxy(callback) {
      this.items = [];
      this.count = 0;

      this.page = 1;
      this.perPage = 10;

      this.sortBy = 'id';
      this.reverse = false;

      this.callback = callback;
    }

    ListHelperProxy.prototype.sort = function(sortBy, reverse) {
      this.page = 1;
      this.sortBy = sortBy;
      this.reverse = reverse;
      this.load();
    };

    ListHelperProxy.prototype.getSortBy = function() {
      return this.sortBy;
    };

    ListHelperProxy.prototype.getReverse = function() {
      return this.reverse;
    };

    ListHelperProxy.prototype.getPage = function() {
      return this.page;
    };

    ListHelperProxy.prototype.setPage = function(page) {
      this.page = page;
      this.load();
    };

    ListHelperProxy.prototype.getPerPage = function() {
      return this.perPage;
    };

    ListHelperProxy.prototype.setPerPage = function(perPage) {
      this.perPage = perPage;
      this.load();
    };

    ListHelperProxy.prototype.getTotalPages = function() {
      return Math.ceil(this.getCount() / this.getPerPage());
    };

    ListHelperProxy.prototype.setCount = function(count) {
      this.count = count;
    };

    ListHelperProxy.prototype.getCount = function() {
      return this.count;
    };

    ListHelperProxy.prototype.setItems = function(items) {
      this.items = items;
    };

    ListHelperProxy.prototype.getItems = function() {
      return this.items;
    };

    ListHelperProxy.prototype.getParams = function() {
      var params = {
        page: this.getPage(),
        perPage: this.getPerPage()
      };

      if (this.getReverse()) {
        params.sort = '-' + this.getSortBy();
      } else {
        params.sort = this.getSortBy();
      }

      return params;
    };

    ListHelperProxy.prototype.load = function() {
      var params = this.getParams();
      this.callback(this, params);
    };

    return ListHelperProxy;
  })
})();
