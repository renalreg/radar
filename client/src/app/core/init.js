(function() {
  'use strict';

  var app = angular.module('radar.core');

  app.factory('init', function(authStore, session, store, $q) {
    var promises = [];

    var userId = authStore.getUserId();

    if (userId !== null) {
      promises.push(store.get('users', userId).then(function(user) {
        session.setUser(user);
      }));
    }

    return $q.all(promises);
  });

  app.run(function(init, $rootScope) {
    $rootScope.init = false;

    init.then(function() {
      $rootScope.init = true;
    });
  });
})();


