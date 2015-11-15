(function() {
  'use strict';

  var app = angular.module('radar.recruitPatient');

  app.directive('recruitPatientPermission', ['AdminPermission', '$compile', function(AdminPermission, $compile) {
    return {
      scope: true,
      link: function(scope, element, attrs) {
        var adminPermission = new AdminPermission();

        scope.$watch(function() {
          return adminPermission.hasPermission();
        }, function(hasPermission) {
          scope.hasPermission = hasPermission;
        });

        // TODO this will overwrite an existing ng-if attribute
        element.attr('ng-if', 'hasPermission');
        element.removeAttr('recruit-patient-permission');
        $compile(element)(scope);
      }
    };
  }]);
})();
