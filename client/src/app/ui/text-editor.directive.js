// jshint camelcase: false
// jscs:disable requireCamelCaseOrUpperCaseIdentifiers

(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('textEditor', ['tinymce', '$sce', '$rootScope', '$timeout', function(tinymce, $sce, $rootScope, $timeout) {
    var nextId = 0;

    return {
      restrict: 'A',
      require: ['ngModel', '?^form'],
      link: function(scope, element, attrs, ctrls) {
        var ngModelCtrl = ctrls[0];
        var formCtrl = ctrls[1];

        var instance;

        var id = 'text-editor-' + nextId++;
        attrs.$set('id', id);

        ngModelCtrl.$render = function() {
          updateUi();
        };

        ngModelCtrl.$formatters.unshift(function(modelValue) {
          return modelValue ? $sce.trustAsHtml(modelValue) : '';
        });

        ngModelCtrl.$parsers.unshift(function(viewValue) {
          return viewValue ? $sce.getTrustedHtml(viewValue) : '';
        });

        scope.$on('$destroy', function() {
          var instance = getInstance();

          if (instance) {
            instance.remove();
            instance = null;
          }
        });

        $timeout(function() {
          tinymce.init({
            selector: '#' + id,
            menubar: false,
            toolbar: 'bold italic | link unlink | bullist numlist | code',
            valid_elements: 'a[href|target=_blank],br,em,li,ol,p,strong,ul',
            plugins: ['link', 'code'],
            setup: function(editor) {
              editor.on('init', function() {
                ngModelCtrl.$render();
                ngModelCtrl.$setPristine();

                if (formCtrl) {
                  formCtrl.$setPristine();
                }

                scope.$apply();
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
        });

        function getInstance() {
          if (!instance) {
            instance = tinymce.get(id);
          }

          return instance;
        }

        function updateUi() {
          var instance = getInstance();

          if (instance) {
            var viewValue = $sce.getTrustedHtml(ngModelCtrl.$viewValue || '');
            instance.setContent(viewValue);
            instance.fire('change');
          }
        }

        function updateView(editor) {
          var content = editor.getContent().trim();
          content = $sce.trustAsHtml(content);
          ngModelCtrl.$setViewValue(content);

          if (!$rootScope.$$phase) {
            scope.$apply();
          }
        }
      }
    };
  }]);
})();
