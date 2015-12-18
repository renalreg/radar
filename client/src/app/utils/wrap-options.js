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
    return function toRadioModel(options, viewValue) {
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

  app.factory('toSelectModel', function() {
    return function toSelectModel(option) {
      if (option === null || option === undefined) {
        return null;
      } else {
        return option.value;
      }
    };
  });

  app.factory('toSelectView', ['_', '$parse', function(_, $parse) {
    return function toSelectView(option, idExpression, labelExpression) {
      if (option === null || option === undefined) {
        option = null;
      } else if (angular.isObject(option)) {
        if (idExpression === undefined) {
          idExpression = 'id';
        }

        if (labelExpression === undefined) {
          labelExpression = 'label';
        }

        var idGetter = $parse(idExpression);
        var labelGetter = $parse(labelExpression);

        option = {
          id: idGetter(option),
          label: labelGetter(option),
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
  }]);

  app.factory('wrapSelectOptions', ['_', 'toSelectView', function(_, toSelectView) {
    return function wrapSelectOptions(options, idPath, labelPath) {
      if (options && options.length) {
        // Convert array (e.g. ['Foo', 'Bar']) into option objects
        // (e.g. [{id: 'Foo', label: 'Foo', value: 'Foo'}, ...])
        options = _.map(options, function(option) {
          return toSelectView(option, idPath, labelPath);
        });
      }

      return options;
    };
  }]);
})();
