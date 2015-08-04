/* globals moment */

(function() {
  'use strict';

  var app = angular.module('moment', []);

  app.factory('moment', function() {
    return moment;
  });
})();
