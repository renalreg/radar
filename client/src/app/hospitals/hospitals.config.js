(function() {
  'use strict';

  var app = angular.module('radar.hospitals');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('hospitals', {
      url: '/hospitals',
      templateUrl: 'app/hospitals/hospital-list.html',
      controller: 'HospitalListController'
    });

    $stateProvider.state('hospital', {
      url: '/hospitals/:hospitalId',
      templateUrl: 'app/hospitals/hospital-detail.html',
      controller: 'HospitalDetailController',
      resolve: {
        hospital: ['$stateParams', 'store', '$q', function($stateParams, store, $q) {
          return store.findOne('groups', $stateParams.hospitalId, true).then(function(group) {
            if (group.type === 'HOSPITAL') {
              return group;
            } else {
              return $q.reject();
            }
          });
        }]
      }
    });
  }]);
})();
