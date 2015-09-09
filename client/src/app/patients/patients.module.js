(function() {
  'use strict';

  angular.module('radar.patients', [
    'ui.router',
    'radar.store',
    'radar.patients.demographics',
    'radar.patients.dialysis',
    'radar.patients.diseaseGroups',
    'radar.patients.genetics',
    'radar.patients.hospitalisations',
    'radar.patients.medications',
    'radar.patients.navigation',
    'radar.patients.renalImaging',
    'radar.patients.saltWasting',
    'radar.patients.plasmapheresis',
    'radar.patients.units'
  ]);
})();
