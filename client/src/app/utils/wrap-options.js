(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('wrapRadioOptions', function(_) {
    return function wrapSelectOptions(options) {
      if (options && options.length) {
        // Convert array of primitives (e.g. ['Foo', 'Bar']) into option objects
        // (e.g. [{label: 'Foo', id: 'Foo'}, ...])
        if (!angular.isObject(options[0])) {
          options = _.map(options, function(x) {
            return {
              label: x,
              id: x
            };
          });
        }
      }

      return options;
    };
  });

  app.factory('unwrapSelectOption', function(_) {
    return function unwrapOption(option) {
      if (option) {
        return option.value;
      } else {
        return option;
      }
    };
  });

  app.factory('wrapSelectOption', function() {
    return function wrapOption(option) {
      if (angular.isObject(option)) {
        option = {
          label: option.label,
          value: option
        };
      } else {
        option = {
          label: option,
          value: option
        };
      }

      return option;
    };
  });

  app.factory('wrapSelectOptions', function(_) {
    return function wrapSelectOptions(options) {
      if (options && options.length) {
        // Convert array of primitives (e.g. ['Foo', 'Bar']) into option objects
        // (e.g. [{label: 'Foo', value: 'Foo'}, ...])
        if (angular.isObject(options[0])) {
          options = _.map(options, function(x) {
            return {
              label: x.label,
              value: x
            };
          });
        } else {
          options = _.map(options, function(x) {
            return {
              label: x,
              value: x
            };
          });
        }
      }

      return options;
    };
  });
})();

