(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmControl', function() {
    return {
      require: '?^frmLayout',
      templateUrl: 'app/forms/control.html',
      replace: true,
      transclude: true,
      link: function(scope, element, attrs, layoutCtrl) {
        scope.horizontal = !layoutCtrl || layoutCtrl.layout === 'horizontal';
      }
    };
  });
})();
