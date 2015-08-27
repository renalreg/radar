(function() {
  'use strict';

  angular.module('radar', [
    'ngCookies',
    'ui.router',
    'radar.auth',
    'radar.controllers',
    'radar.core',
    'radar.demographics',
    'radar.dialysis',
    'radar.diseaseGroups',
    'radar.filters',
    'radar.forms',
    'radar.patients',
    'radar.posts',
    'radar.store',
    'radar.units',
    'radar.users',
    'radar.utils',
    'radar.hello'
  ]);
})();
