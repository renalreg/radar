(function() {
  'use strict';

  angular.module('radar', [
    'ui.router',

    'radar.controllers',
    'radar.core',
    'radar.filters',
    'radar.forms',
    'radar.store',
    'radar.utils',

    'radar.patients',
    'radar.posts',
    'radar.users',

    'radar.demographics',
    'radar.dialysis',
    'radar.diseaseGroups',
    'radar.units',

    'radar.hello'
  ]);
})();
