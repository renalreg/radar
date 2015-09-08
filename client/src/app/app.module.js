(function() {
  'use strict';

  // TODO move dependencies to modules
  angular.module('radar', [
    'ngCookies',
    'ui.router',
    'radar.account',
    'radar.auth',
    'radar.controllers',
    'radar.core',
    'radar.fields',
    'radar.filters',
    'radar.forms',
    'radar.patients',
    'radar.permissions',
    'radar.posts',
    'radar.store',
    'radar.ui',
    'radar.users',
    'radar.utils',
    'radar.validators'
  ]);
})();
