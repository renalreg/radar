(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmLabel', function() {
    return {
      require: '?^frmLayout',
      templateUrl: 'app/forms/label.html',
      replace: true,
      transclude: true,
      link: function(scope, element, attrs, layoutCtrl) {
        scope.horizontal = !layoutCtrl || layoutCtrl.layout === 'horizontal';
      }
    };
  });
})();
