(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmButtons', function() {
    return {
      require: '?^frmLayout',
      templateUrl: 'app/forms/buttons.html',
      transclude: true,
      link: function(scope, element, attrs, layoutCtrl) {
        scope.horizontal = !layoutCtrl || layoutCtrl.layout === 'horizontal';
      }
    };
  });
})();
