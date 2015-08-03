(function() {
  'use strict';

  angular.module('radar', [
    'radar.core',
    'radar.patients',
    'radar.diseaseGroups',
    'radar.units',
    'radar.demographics',
    'radar.dialysis',
    'radar.form',
    'ui.router',
    'ngResource'
  ]);
})();
