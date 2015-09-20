(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('frmModel', function() {
    return {
      require: ['^frmField', 'ngModel'],
      link: function(scope, element, attrs, ctrls) {
        var fieldCtrl = ctrls[0];
        var ngModelCtrl = ctrls[1];
        fieldCtrl.setModelCtrl(ngModelCtrl);
      }
    };
  });
})();
