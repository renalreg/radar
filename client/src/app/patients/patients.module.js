(function() {
  'use strict';

  angular.module('radar.patients', [
    'ui.router',
    'radar.store',
    'radar.patients.cohorts',
    'radar.patients.demographics',
    'radar.patients.diagnoses',
    'radar.patients.dialysis',
    'radar.patients.genetics',
    'radar.patients.hospitalisations',
    'radar.patients.medications',
    'radar.patients.navigation',
    'radar.patients.pathology',
    'radar.patients.plasmapheresis',
    'radar.patients.renalImaging',
    'radar.patients.saltWasting',
    'radar.patients.transplants',
    'radar.patients.units'
  ]);
})();
