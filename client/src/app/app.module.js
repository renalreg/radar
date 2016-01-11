(function() {
  'use strict';

  angular.module('radar', [
    'LocalStorageModule',
    'ui.router',
    'radar.account',
    'radar.auth',
    'radar.cohorts',
    'radar.consultants',
    'radar.controllers',
    'radar.core',
    'radar.crud',
    'radar.filters',
    'radar.forms',
    'radar.groups',
    'radar.home',
    'radar.hospitals',
    'radar.logs',
    'radar.notifications',
    'radar.observations',
    'radar.patients',
    'radar.permissions',
    'radar.posts',
    'radar.recruitPatient',
    'radar.sessions',
    'radar.sources',
    'radar.store',
    'radar.ui',
    'radar.users',
    'radar.utils',
    'radar.validators'
  ]);
})();
