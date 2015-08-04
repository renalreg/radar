(function() {
  'use strict';

  var app = angular.module('radar.form');

  app.directive('rrDeleteButton', function($window, $q) {
    return {
      restrict: 'A',
      scope: {
        action: '&'
      },
      templateUrl: 'app/form/delete-button.html',
      link: function(scope, element) {
        scope.deleting = false;

        element.on('click', function() {
          if ($window.confirm('Are you sure?')) {
            scope.$apply(remove);
          }
        });

        function remove() {
          scope.deleting = true;

          $q.when(scope.action()).then(function() {
            scope.deleting = false;
          });
        }
      }
    };
  });
})();
