/* globals zxcvbn */

(function() {
  'use strict';

  var app = angular.module('zxcvbn', []);

  app.constant('zxcvbn', zxcvbn);
})();
