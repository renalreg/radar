(function() {
  'use strict';

  angular.module('radar.patients', [
    'ui.router',
    'radar.store',
    'radar.patients.demographics',
    'radar.patients.dialysis',
    'radar.patients.diseaseGroups',
    'radar.patients.medications',
    'radar.patients.navigation',
    'radar.patients.units'
  ]);
})();
