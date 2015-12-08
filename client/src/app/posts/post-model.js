(function() {
  'use strict';

  var app = angular.module('radar.posts');

  app.factory('PostModel', ['Model', 'safeHtml', function(Model, safeHtml) {
    function PostModel(modelName, data) {
      data.body = safeHtml(data.body);
      Model.call(this, modelName, data);
    }

    PostModel.prototype = Object.create(Model.prototype);

    return PostModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('posts', 'PostModel');
  }]);
})();
