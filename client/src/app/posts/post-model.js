(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.factory('PostModel', ['Model', '$sce', function(Model, $sce) {
    function PostModel(modelName, data) {
      Model.call(this, modelName, data);
    }

    PostModel.prototype = Object.create(Model.prototype);

    PostModel.prototype.getHtml = function() {
      var body = this.body || '';
      return $sce.trustAsHtml(body);
    };

    return PostModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('posts', 'PostModel');
  }]);
})();
