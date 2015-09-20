/* globals md5 */

(function() {
  'use strict';

  var app = angular.module('md5', []);

  app.factory('md5', function() {
    return md5;
  });
})();
