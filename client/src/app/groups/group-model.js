(function() {
  'use strict';

  var app = angular.module('radar.groups');

  app.factory('GroupModel', ['Model', 'safeHtml', function(Model, safeHtml) {
    function GroupModel(modelName, data) {
      // Mark the notes HTML as safe
      data.notes = safeHtml(data.notes);

      Model.call(this, modelName, data);
    }

    GroupModel.prototype = Object.create(Model.prototype);

    return GroupModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('groups', 'GroupModel');
  }]);
})();
