(function() {
  'use strict';

  var app = angular.module('radar.recruitPatient');

  function recruitPatientPermission(
    hasRecruitPatientPermission,
    $compile,
    session
  ) {
    return {
      scope: true,
      link: function(scope, element, attrs) {
        scope.$watch(function() {
          return hasRecruitPatientPermission(session.user);
        }, function(hasPermission) {
          scope.hasPermission = hasPermission;
        });

        // TODO this will overwrite an existing ng-if attribute
        element.attr('ng-if', 'hasPermission');
        element.removeAttr('recruit-patient-permission');
        $compile(element)(scope);
      }
    };
  }

  recruitPatientPermission.$inject = [
    'hasRecruitPatientPermission',
    '$compile',
    'session'
  ];

  app.directive('recruitPatientPermission', recruitPatientPermission);
})();
