(function() {
  'use strict';

  var app = angular.module('radar.forms.fields');

  app.directive('frmGroupField', ['sortGroups', 'store', function(sortGroups, store) {
    return {
      restrict: 'A',
      scope: {
        model: '=',
        required: '&'
      },
      templateUrl: 'app/forms/fields/group-field.html',
      link: function(scope) {
        store.findMany('groups').then(function(groups) {
          scope.groups = sortGroups(groups);
        });
      }
    };
  }]);
})();
