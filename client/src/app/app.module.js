(function() {
  'use strict';

  angular.module('radar', [
    'ngCookies',
    'ui.router',
    'radar.account',
    'radar.auth',
    'radar.controllers',
    'radar.core',
    'radar.demographics',
    'radar.dialysis',
    'radar.diseaseGroups',
    'radar.fields',
    'radar.filters',
    'radar.forms',
    'radar.patients',
    'radar.permissions',
    'radar.posts',
    'radar.store',
    'radar.ui',
    'radar.units',
    'radar.users',
    'radar.utils',
    'radar.validation'
  ]);
})();
