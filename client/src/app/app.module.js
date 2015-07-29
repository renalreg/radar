(function() {
  'use strict';

  angular.module('radar', [
    'radar.patient',
    'radar.demographics',
    'radar.dialysis',
    'ui.router',
    'restangular'
  ]);
})();
