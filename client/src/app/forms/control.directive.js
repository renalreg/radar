(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmControl', function() {
    return {
      require: ['^frmField', '?^frmLayout'],
      templateUrl: 'app/forms/control.html',
      replace: true,
      transclude: true,
      link: function(scope, element, attrs, ctrls) {
        var fieldCtrl = ctrls[0];
        var layoutCtrl = ctrls[1];

        scope.$watch(function() {
          return fieldCtrl.hasLabel();
        }, function(value) {
          scope.hasLabel = value;
        });

        scope.horizontal = !layoutCtrl || layoutCtrl.layout === 'horizontal';
      }
    };
  });
})();
