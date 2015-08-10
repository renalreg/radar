(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.factory('ListService', function($q, $filter, lodash, $rootScope) {
    function ListService(listFunction) {
      var self = this;

      self.listFunction = listFunction;

      self.deletedItems = [];

      // List
      self.items = [];
      self.filteredItems = [];
      self.sortedItems = [];
      self.displayItems = [];

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
        self.page = 1;
        self.filter();
      });

      $rootScope.$watch(function() {
        return self.sortBy;
      }, function() {
        self.page = 1;
        self.sort();
      });

      $rootScope.$watch(function() {
        return self.reverse;
      }, function() {
        self.page = 1;
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
        self.page = 1;
        self.paginate();
      });

      this.load();
    }

    ListService.prototype.load = function() {
      var self = this;

      // Empty the items list
      this.items = [];
      this.filter();

      this.isLoading = true;

      $q.when(this.listFunction()).then(function(items) {
        self.items = items;
        self.isLoading = false;
        self.filter();
      });
    };

    ListService.prototype.filter = function() {
      var filteredItems = this.items;

      if (this.search) {
        filteredItems = $filter('filter')(filteredItems, this.search);
      }

      this.filteredItems = filteredItems;

      this.sort();
    };

    ListService.prototype.sort = function() {
      var sortedItems = lodash.sortBy(this.filteredItems, this.sortBy);

      if (this.reverse) {
        sortedItems.reverse();
      }

      this.sortedItems = sortedItems;

      this.paginate();
    };

    ListService.prototype.paginate = function() {
      var startIndex = (this.page - 1) * this.perPage;
      var endIndex = this.page * this.perPage;
      this.displayItems = lodash.slice(this.sortedItems, startIndex, endIndex);
    };

    ListService.prototype.add = function(item) {
      console.log(item);

      if (this.items.indexOf(item) === -1) {
        console.log('Added!');
        this.items.push(item);
        this.filter();
      }
    };

    ListService.prototype.isDeleted = function(item) {
      return this.deletedItems.indexOf(item) >= 0;
    };

    ListService.prototype.remove = function(item) {
      var self = this;

      self.deletedItems.push(item);

      var promise = item.$delete();

      promise.then(function() {
        lodash.pull(self.items, item);
        lodash.pull(self.deletedItems, item);
        self.filter();
      });

      return promise;
    };

    return ListService;
  });
})();
