(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('safeHtml', ['$sce', function($sce) {
    return function safeHtml(value) {
      if (angular.isObject(value)) {
        value = $sce.getTrustedHtml(value);
      }

      value = $sce.trustAsHtml(value || '');

      return value;
    };
  }]);
})();
