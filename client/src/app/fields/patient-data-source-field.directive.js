(function() {
  'use strict';

  var app = angular.module('radar.fields');

  app.directive('frmPatientDataSourceField', function(store, session, _) {
    return {
      restrict: 'A',
      scope: {
        patient: '=',
        model: '=',
        required: '&'
      },
      templateUrl: 'app/fields/patient-data-source-field.html',
      link: function(scope) {
        var user = session.user;
        var isAdmin = user.isAdmin;

        var organisationIds = [];

        if (!isAdmin) {
          _.forEach(user.organisations, function(organistion) {
            if (organistion.hasEditPatientPermission) {
              organisationIds.push(organistion.organistion.id);
            }
          });
        }

        var dataSources = [];
        var patientOrganisations = scope.patient.organisations;

        _.forEach(patientOrganisations, function(organisation) {
          if (isAdmin || organisationIds.indexOf(organisation.organisation.id) >= 0) {
            _.forEach(organisation.organisation.dataSources, function(dataSource) {
              if (dataSource.type === 'RADAR') {
                dataSources.push(dataSource);
              }
            });
          }
        });

        dataSources = _.sortBy(dataSources, function(x) {
          return x.getName();
        });

        if (!scope.model) {
          scope.model = dataSources[0];
        }

        scope.dataSources = dataSources;
      }
    };
  });
})();
