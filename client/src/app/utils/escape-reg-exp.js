(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('escapeRegExp', function(_) {
    return function escapeRegExp(string) {
      return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    };
  });
})();

