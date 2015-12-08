(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmPatientDataSourceField', ['sortDataSources', 'store', 'session', '_', function(sortDataSources, store, session, _) {
    return {
      restrict: 'A',
      scope: {
        patient: '=',
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/patient-data-source-field.html',
      link: function(scope) {
        var user = session.user;
        var isAdmin = user.isAdmin;

        var organisationIds = [];

        if (!isAdmin) {
          var userOrganisations = user.organisations;

          _.forEach(userOrganisations, function(organisation) {
            if (organisation.hasPermission('EDIT_PATIENT')) {
              organisationIds.push(organisation.organisation.id);
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

        dataSources = sortDataSources(dataSources);

        if (!scope.model) {
          scope.model = dataSources[0];
        }

        scope.dataSources = dataSources;
      }
    };
  }]);
})();
