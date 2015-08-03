(function() {
  'use strict';

  var app = angular.module('radar.diseaseGroups');

  app.config(function($stateProvider) {
    $stateProvider.state('patient.diseaseGroups', {
      url: '/disease-groups',
      templateUrl: 'app/disease-groups/disease-group-list.html',
      controller: 'DiseaseGroupListController'
    });
  });
})();
