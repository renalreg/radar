(function() {
  'use strict';

  var app = angular.module('radar.sources');

  app.factory('SourceModelMixin', ['_', function(_) {
    return {
      getSource: function() {
        return this.sourceGroup.shortName + ' (' + this.sourceType + ')';
      }
    };
  }]);
})();
