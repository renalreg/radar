/* globals md5 */

(function() {
  'use strict';

  var app = angular.module('md5', []);

  app.constant('md5', md5);
})();
