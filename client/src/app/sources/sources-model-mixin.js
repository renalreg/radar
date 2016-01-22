(function() {
  'use strict';

  var app = angular.module('radar.sources');

  app.factory('SourceModelMixin', ['_', function(_) {
    return {
      getSource: function() {
        if (this.sourceGroup.shortName) {
          return this.sourceGroup.shortName + ' (' + this.sourceType + ')';
        } else {
          return this.sourceType;
        }
      }
    };
  }]);
})();
