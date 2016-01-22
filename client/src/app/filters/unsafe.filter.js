
(function() {
  'use strict';

  var app = angular.module('radar.filters');

  app.filter('unsafe', ['$sce', function($sce) {
    return $sce.trustAsHtml;
  }]);
})();
