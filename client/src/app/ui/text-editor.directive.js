// jshint camelcase: false
// jscs:disable requireCamelCaseOrUpperCaseIdentifiers

(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('textEditor', ['tinymce', '$sce', function(tinymce, $sce) {
    var nextId = 0;

    return {
      restrict: 'A',
      require: 'ngModel',
      link: function(scope, element, attrs, ngModel) {
        var instance;

        var id = 'text-editor-' + nextId++;
        attrs.$set('id', id);

        ngModel.$render = function() {
          var instance = getInstance();

          if (instance) {
            var viewValue = ngModel.$viewValue;
            viewValue = viewValue ? $sce.getTrustedHtml(viewValue) : '';
            instance.setContent(viewValue);
            instance.fire('change');
          }
        };

        ngModel.$formatters.unshift(function(modelValue) {
          return modelValue ? $sce.trustAsHtml(modelValue) : '';
        });

        ngModel.$parsers.unshift(function(viewValue) {
          return viewValue ? $sce.getTrustedHtml(viewValue) : '';
        });

        scope.$on('$destroy', function() {
          var instance = getInstance();

          if (instance) {
            instance.remove();
            instance = null;
          }
        });

        tinymce.init({
          selector: '#' + id,
          menubar: false,
          toolbar: 'bold italic | link unlink | bullist numlist | code',
          valid_elements: 'a[href|target=_blank],br,em,li,ol,p,strong,ul',
          plugins: ['link', 'code'],
          setup: function(editor) {
            editor.on('init', function() {
              ngModel.$render();
              ngModel.$setPristine();
            });

            editor.on('keyup', function() {
              updateView(editor);
            });

            // Content changed using toolbar buttons
            editor.on('change', function() {
              updateView(editor);
            });
          }
        });

        function getInstance() {
          if (!instance) {
            instance = tinymce.get(id);
          }

          return instance;
        }

        function updateView(editor) {
          var content = editor.getContent().trim();
          content = $sce.trustAsHtml(content);
          ngModel.$setViewValue(content);
          scope.$apply();
        }
      }
    };
  }]);
})();
