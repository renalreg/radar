(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmDiseaseGroupField', function(_, session, store) {
    function sortDiseaseGroups(diseaseGroups) {
      return _.sortBy(diseaseGroups, function(x) {
        return x.name.toUpperCase();
      });
    }

    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '='
      },
      templateUrl: 'app/fields/disease-group-field.html',
      link: function(scope) {
        var user = session.user;

        if (user.isAdmin) {
          store.findMany('disease-groups').then(function(diseaseGroups) {
            scope.diseaseGroups = sortDiseaseGroups(diseaseGroups);
          });
        } else {
          var diseaseGroups = session.user.diseaseGroups;
          scope.diseaseGroups = sortDiseaseGroups(diseaseGroups);
        }
      }
    };
  });
})();

