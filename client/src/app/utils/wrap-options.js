(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('wrapRadioOptions', function(_) {
    return function wrapRadioOptions(options) {
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
          id: option.id,
          label: option.label,
          value: option
        };
      } else {
        option = {
          id: option,
          label: option,
          value: option
        };
      }

      return option;
    };
  });

  app.factory('wrapSelectOptions', function(_, wrapSelectOption) {
    return function wrapSelectOptions(options) {
      if (options) {
        // Convert array (e.g. ['Foo', 'Bar']) into option objects
        // (e.g. [{id: 'Foo', label: 'Foo', value: 'Foo'}, ...])
        options = _.map(options, wrapSelectOption);
      }

      return options;
    };
  });
})();

