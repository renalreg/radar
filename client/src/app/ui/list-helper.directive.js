(function() {
  'use strict';

  var app = angular.module('radar.ui');

  var DEFAULT_PER_PAGE = 10;

  app.directive('listHelper', ['$parse', '_', 'escapeRegExp', 'dateSearch', 'anyValue', function($parse, _, escapeRegExp, dateSearch, anyValue) {
    return {
      scope: false,
      controller: ['$scope', '$attrs', function($scope, $attrs) {
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
          var sortScope = $scope;
          var sortId = null;
          var reverse = false;

          var page = 1;
          var perPage = DEFAULT_PER_PAGE;

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

          $attrs.$observe('sortBy', function(value) {
            if (value) {
              sortBy = value;
              _sort();
              sortId = value;
            }
          });

          $attrs.$observe('reverse', function(value) {
            if (value) {
              reverse = value === 'true';
              _sort();
            }
          });

          $scope.$watch('items', function() {
            _filter();
          }, true);

          _filter();

          self.sort = sort;
          self.filter = filter;
          self.getSortBy = getSortBy;
          self.getReverse = getReverse;
          self.getSortId = getSortId;
          self.getPage = getPage;
          self.setPage = setPage;
          self.getPerPage = getPerPage;
          self.setPerPage = setPerPage;
          self.getTotalPages = getTotalPages;
          self.getCount = getCount;
          self.getItems = getItems;

          function sort(newSortBy, newReverse, newSortId, newSortScope) {
            sortBy = newSortBy;
            reverse = newReverse;
            sortId = newSortId;
            sortScope = newSortScope;
            page = 1;
            _sort();
          }

          function filter(newSearch) {
            search = newSearch;
            _filter();
          }

          function getSortId() {
            return sortId;
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
              var searchRegExp = new RegExp(escapeRegExp(search.trim()), 'i');
              var searchMatcher = function(value) {
                return searchRegExp.test(value);
              };

              var dateMatcher = dateSearch(search);

              var matcher = function(value) {
                return searchMatcher(value) || dateMatcher(value);
              };

              filteredItems = _.filter(filteredItems, function(x) {
                return anyValue(x.getData(), matcher);
              });
            }

            _sort();
          }

          function _sort() {
            sortedItems = filteredItems;

            if (sortBy !== null) {
              var getter = $parse(sortBy);

              sortedItems = _.sortBy(sortedItems, function(item) {
                // Note: AngularJS doesn't check the prototype of the locals argument
                return getter(item, sortScope);
              });
            }

            if (reverse) {
              sortedItems.reverse();
            }

            _paginate();
          }

          function _paginate() {
            if (perPage === null) {
              paginatedItems = sortedItems;
            } else {
              var startIndex = (page - 1) * perPage;
              var endIndex = page * perPage;
              paginatedItems = _.slice(sortedItems, startIndex, endIndex);
            }

          }
        }

        function server(apiGetter) {
          var api = apiGetter($scope);

          $scope.$watch(function() {
            return apiGetter($scope);
          }, function(value) {
            api = value;
          });

          self.sort = sort;
          self.getSortBy = getSortBy;
          self.getReverse = getReverse;
          self.getSortId = getSortId;
          self.getPage = getPage;
          self.setPage = setPage;
          self.getPerPage = getPerPage;
          self.setPerPage = setPerPage;
          self.getTotalPages = getTotalPages;
          self.getCount = getCount;
          self.getItems = getItems;

          function sort(sortBy, reverse) {
            if (api) {
              api.sort(sortBy, reverse);
            }
          }

          function getSortId() {
            return getSortBy();
          }

          function getSortBy() {
            return api ? api.getSortBy() : 'id';
          }

          function getReverse() {
            return api ? api.getReverse() : false;
          }

          function getPage() {
            return api ? api.getPage() : 1;
          }

          function setPage(page) {
            if (api) {
              api.setPage(page);
            }
          }

          function getPerPage() {
            return api ? api.getPerPage() : DEFAULT_PER_PAGE;
          }

          function setPerPage(perPage) {
            if (api) {
              api.setPerPage(perPage);
            }
          }

          function getTotalPages() {
            return api ? api.getTotalPages() : 0;
          }

          function getCount() {
            return api ? api.getCount() : 0;
          }

          function getItems() {
            return api ? api.getItems() : [];
          }
        }
      }]
    };
  }]);

  app.factory('ListHelperProxy', function() {
    function ListHelperProxy(callback, params) {
      this.items = [];
      this.count = 0;

      this.page = 1;
      this.perPage = DEFAULT_PER_PAGE;

      this.sortBy = 'id';
      this.reverse = false;

      this.callback = callback;

      if (params) {
        if (params.perPage) {
          this.perPage = params.perPage;
        }

        if (params.sortBy) {
          this.sortBy = params.sortBy;
        }

        if (params.reverse) {
          this.reverse = params.reverse;
        }
      }
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
  });
})();
