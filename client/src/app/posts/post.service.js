(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.factory('PostService', function(endpointFactory) {
    var Endpoint = endpointFactory('/posts/:id', {
      params: {
        'id': '@id'
      }
    });

    return {
      getList: getList,
      create: create
    };

    function create(data) {
      return new Endpoint(data);
    }

    function getList() {
      return Endpoint.query().$promise;
    }
  });
})();

