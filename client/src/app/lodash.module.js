/* globals _ */

(function() {
  'use strict';

  var app = angular.module('lodash', []);

  app.factory('lodash', function() {
    return _;
  });
})();

