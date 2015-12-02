(function() {
  'use strict';

  var app = angular.module('radar.forms');

  app.directive('submitButton', function() {
    return {
      require: ['^form', '?^submitIfValid'],
      scope: {},
      transclude: true,
      templateUrl: 'app/forms/submit-button.html',
      link: function(scope, element, attrs, ctrls) {
        var formCtrl = ctrls[0];
        var submitIfValidCtrl = ctrls[1];

        scope.formCtrl = formCtrl;
        scope.submitting = false;

        if (submitIfValidCtrl !== null) {
          submitIfValidCtrl.on('submit', function() {
            scope.submitting = true;
          });

          submitIfValidCtrl.on('done', function() {
            scope.submitting = false;
          });
        }
      }
    };
  });
})();
