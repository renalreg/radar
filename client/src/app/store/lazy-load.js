(function() {
  'use strict';

  var app = angular.module('radar.store');

  app.factory('lazyLoad', ['_', 'store', function(_, store) {
    return function lazyLoad(modelName, data) {
      var item;

      if (_.isInteger(data)) {
        var id = data;

        item = store.getFromStore(modelName, id);

        if (item === null) {
          item = store.create(modelName, {id: id});
          item = store.pushToStore(item);
          item.reload();
        }
      } else if (data) {
        item = store.pushToStore(store.create(modelName, data));
      } else {
        item = data;
      }

      return item;
    };
  }]);
})();
