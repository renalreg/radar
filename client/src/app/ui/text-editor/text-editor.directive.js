// jshint camelcase: false
// jscs:disable requireCamelCaseOrUpperCaseIdentifiers

(function() {
  'use strict';

  var app = angular.module('radar.ui.textEditor');

  app.directive('textEditor', ['Quill', '$sce', function(Quill, $sce) {
    return {
      restrict: 'A',
      require: 'ngModel',
      templateUrl: 'app/ui/text-editor/text-editor.html',
      link: function(scope, element, attrs, ngModel) {
        var container = element.find('.text-editor').get(0);
        var toolbar = element.find('.text-editor-toolbar').get(0);

        var quill = new Quill(container, {
          styles: false,
          formats: ['bold', 'italic', 'link', 'bullet', 'list']
        });
        quill.addModule('toolbar', {container: toolbar});
        quill.addModule('link-tooltip', true);

        ngModel.$render = function() {
          quill.setHTML(ngModel.$viewValue || '');
        };

        quill.on('text-change', function() {
          scope.$apply(function() {
            var html = quill.getHTML();
            ngModel.$setViewValue(html);
          });
        });
      }
    };
  }]);
})();
