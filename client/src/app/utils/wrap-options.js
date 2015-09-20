(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('toRadioView', function() {
    return function toRadioView(modelValue) {
      if (angular.isObject(modelValue)) {
        return modelValue.id;
      } else {
        return modelValue;
      }
    };
  });

  app.factory('toRadioModel', function() {
    return function toRadioView(options, viewValue) {
      for (var i = 0; i < options.length; i++) {
        var option = options[i];

        if (angular.isObject(option)) {
          if (option.id === viewValue) {
            return option;
          }
        } else {
          if (option === viewValue) {
            return option;
          }
        }
      }

      return null;
    };
  });

  app.factory('wrapRadioOptions', ['_', function(_) {
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
  }]);

  app.factory('unwrapSelectOption', function() {
    return function unwrapOption(option) {
      if (option) {
        return option.value;
      } else {
        return option;
      }
    };
  });

  app.factory('wrapSelectOption', function() {
    return function wrapSelectOption(option) {
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

  app.factory('wrapSelectOptions', ['_', 'wrapSelectOption', function(_, wrapSelectOption) {
    return function wrapSelectOptions(options) {
      if (options) {
        // Convert array (e.g. ['Foo', 'Bar']) into option objects
        // (e.g. [{id: 'Foo', label: 'Foo', value: 'Foo'}, ...])
        options = _.map(options, wrapSelectOption);
      }

      return options;
    };
  }]);
})();

