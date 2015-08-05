(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.factory('ListService', function($q, $filter, lodash, $rootScope) {
    function ListService(listFunction) {
      var self = this;

      self.listFunction = listFunction;

      // List
      self._items = [];
      self._filteredItems = [];
      self._sortedItems = [];
      self.items = [];

      // Filtering
      self.search = null;

      // Sorting
      self.sortBy = 'id';
      self.reverse = false;

      // Pagination
      self.page = 1;
      self.perPage = 5;

      $rootScope.$watch(function() {
        return self.search;
      }, function() {
        self.filter();
      });

      $rootScope.$watch(function() {
        return self.sortBy;
      }, function() {
        self.sort();
      });

      $rootScope.$watch(function() {
        return self.reverse;
      }, function() {
        self.sort();
      });

      $rootScope.$watch(function() {
        return self.page;
      }, function() {
        self.paginate();
      });

      $rootScope.$watch(function() {
        return self.perPage;
      }, function() {
        self.paginate();
      });

      this.load();
    }

    ListService.prototype.load = function() {
      var self = this;

      // Empty the items list
      this._items = [];
      this.filter();

      this.isLoading = true;

      $q.when(this.listFunction()).then(function(items) {
        self._items = items;
        self.isLoading = false;
        self.filter();
      });
    };

    ListService.prototype.filter = function() {
      var filteredItems = this._items;

      if (this.search) {
        filteredItems = $filter('filter')(filteredItems, this.search);
      }

      this._filteredItems = filteredItems;

      this.sort();
    };

    ListService.prototype.sort = function() {
      this.page = 1;

      var sortedItems = lodash.sortBy(this._filteredItems, this.sortBy);

      if (this.reverse) {
        sortedItems.reverse();
      }

      this._sortedItems = sortedItems;

      this.paginate();
    };

    ListService.prototype.paginate = function() {
      var startIndex = (this.page - 1) * this.perPage;
      var endIndex = this.page * this.perPage;
      this.items = lodash.slice(this._sortedItems, startIndex, endIndex);
    };

    return ListService;
  });
})();
