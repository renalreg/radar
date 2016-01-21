(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmHospitalField', ['_', 'session', 'hospitalStore', 'sortHospitals', function(_, session, hospitalStore, sortHospitals) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/hospital-field.html',
      link: function(scope) {
        scope.$watch(function() {
          return session.user;
        }, function(user) {
          if (user) {
            if (user.isAdmin) {
              hospitalStore.findMany().then(setHospitals);
            } else {
              var hospitals = user.getHospitals();
              setHospitals(hospitals);
            }
          } else {
            setHospitals([]);
          }
        });

        function setHospitals(hospitals) {
          scope.hospitals = sortHospitals(hospitals);
        }
      }
    };
  }]);
})();
