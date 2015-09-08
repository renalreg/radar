(function() {
  'use strict';

  angular.module('radar.patients', [
    'ui.router',
    'radar.store',
    'radar.patients.demographics',
    'radar.patients.dialysis',
    'radar.patients.diseaseGroups',
    'radar.patients.hospitalisations',
    'radar.patients.medications',
    'radar.patients.navigation',
    'radar.patients.plasmapheresis',
    'radar.patients.units'
  ]);
})();
