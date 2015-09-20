(function() {
  'use strict';

  var app = angular.module('radar.store');

  app.factory('hashModel', ['flattenRelationships', '_', 'md5', function(flattenRelationships, _, md5) {
    return function hash(data) {
      data = flattenRelationships(data);
      var values = _hash(data);
      return md5(values.join(''));
    };

    function _hash(data) {
      var keys = _.sortBy(_.keys(data));
      var values = [];

      _.forEach(keys, function(key) {
        var value = data[key];

        if (angular.isArray(value)) {
          _.forEach(value, function(x) {
            values = values.concat(_hash(x));
          });
        } else if (angular.isObject(value)) {
          values = values.concat(_hash(value));
        } else {
          values.push(value);
        }
      });

      return values;
    }
  }]);
})();
