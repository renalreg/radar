(function() {
  'use strict';

  var app = angular.module('radar.recruitPatient');

  function recruitPatientPermission(
    hasPermission,
    $compile,
    session
  ) {
    return {
      scope: true,
      link: function(scope, element, attrs) {
        scope.$watch(function() {
          return hasPermission(session.user, 'RECRUIT_PATIENT');
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
    'hasPermission',
    '$compile',
    'session'
  ];

  app.directive('recruitPatientPermission', recruitPatientPermission);
})();
