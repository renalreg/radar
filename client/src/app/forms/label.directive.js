(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmLabel', function() {
    return {
      require: ['^frmField', '?^frmLayout'],
      templateUrl: 'app/forms/label.html',
      replace: true,
      transclude: true,
      link: function(scope, element, attrs, ctrls) {
        var fieldCtrl = ctrls[0];
        var layoutCtrl = ctrls[1];
        fieldCtrl.registerLabel();
        scope.horizontal = !layoutCtrl || layoutCtrl.layout === 'horizontal';
      }
    };
  });
})();
