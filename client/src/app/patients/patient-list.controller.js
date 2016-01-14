(function() {
  'use strict';

  var app = angular.module('radar.patients');

  function controllerFactory(
    ListController,
    $injector,
    ListHelperProxy,
    firstPromise,
    store
  ) {
    var DEFAULT_FILTERS = {
      current: true
    };

    function PatientListController($scope) {
      var self = this;

      $injector.invoke(ListController, self, {$scope: $scope});

      $scope.filters = angular.copy(DEFAULT_FILTERS);

      var proxy = new ListHelperProxy(search, {
        perPage: 50,
        sortBy: 'id',
        reverse: true
      });
      proxy.load();

      $scope.proxy = proxy;
      $scope.search = search;
      $scope.clear = clear;
      $scope.count = 0;

      var genderPromise = store.findMany('genders').then(function(genders) {
        $scope.genders = genders;
      });

      function filtersToParams(filters) {
        var params = {};

        var keys = [
            'id',
            'firstName', 'lastName',
            'dateOfBirth', 'yearOfBirth',
            'dateOfDeath', 'yearOfDeath',
            'gender', 'patientNumber',
            'current'
        ];

        _.forEach(keys, function(key) {
          var value = filters[key];

          if (value !== undefined && value !== null && value !== '') {
            params[key] = value;
          }
        });

        var groups = _.filter([filters.cohort, filters.hospital], function(group) {
          return group !== undefined && group !== null;
        });

        var groupIds = _.map(groups, function(group) {
          return group.id;
        });

        if (groupIds.length > 0) {
          params.group = groupIds.join(',');
        }

        console.log(params);

        return params;
      }

      function search() {
        var proxyParams = proxy.getParams();
        var params = angular.extend({}, proxyParams, filtersToParams($scope.filters));

        return self.load(firstPromise([
          store.findMany('patients', params, true).then(function(data) {
            proxy.setItems(data.data);
            proxy.setCount(data.pagination.count);
            $scope.count = data.pagination.count;
            return data.data;
          }),
          genderPromise
        ]));
      }

      function clear() {
        $scope.filters = angular.copy(DEFAULT_FILTERS);
        search();
      }
    }

    PatientListController.$inject = ['$scope'];
    PatientListController.prototype = Object.create(ListController.prototype);

    return PatientListController;
  }

  controllerFactory.$inject = [
    'ListController',
    '$injector',
    'ListHelperProxy',
    'firstPromise',
    'store'
  ];

  app.factory('PatientListController', controllerFactory);
})();
