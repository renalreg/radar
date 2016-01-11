(function() {
  'use strict';

  var app = angular.module('radar.hospitals');

  app.controller('HospitalListController', ['$scope', 'session', 'store', '_', 'sortHospitals', function($scope, session, store, _, sortHospitals) {
    $scope.loading = true;

    var user = session.user;

    if (user.isAdmin) {
      store.findMany('groups', {type: 'HOSPITAL'}).then(function(hospitals) {
        setHospitals(hospitals);
      });
    } else {
      var hospitals = _.filter(user.getHospitals(), function(x) {
        return x.group;
      });

      setHospitals(hospitals);
    }

    function setHospitals(hospitals) {
      $scope.hospitals = sortHospitals(hospitals);
      $scope.loading = false;
    }
  }]);
})();
