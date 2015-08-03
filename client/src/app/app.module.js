(function() {
  'use strict';

  angular.module('radar', [
    'radar.patient',
    'radar.demographics',
    'radar.dialysis',
    'radar.form',
    'ui.router',
    'restangular',
    'ngResource'
  ]);
})();
