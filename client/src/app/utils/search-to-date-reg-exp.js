(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('searchToDateRegExp', function(_) {
    var datePatterns = [
      /^([0-9]+)\/0*$/,
      /^([0-9]+)\/([0-9]+)(?:\/0*)?$/,
      /^([0-9]+)\/([0-9]+)\/([0-9]+)$/,
      /^([0-9]+)\/([0-9]+)\/([0-9]+)\s+([0-9]+)(?::0*)?$/,
      /^([0-9]+)\/([0-9]+)\/([0-9]+)\s+([0-9]+):([0-9]+)(?::0*)?$/,
      /^([0-9]+)\/([0-9]+)\/([0-9]+)\s+([0-9]+):([0-9]+):([0-9]+)$/
    ];

    function searchToDateRegExp(search) {
      search = search.trim();

      for (var i = 0; i < datePatterns.length; i++) {
        var datePattern = datePatterns[i];

        var match = datePattern.exec(search);

        if (match) {
          var dateParts = [];
          var timeParts = [];

          for (var j = 1; j < match.length; j++) {
            var value = parseInt(match[j], 10).toString();

            if (j === 3) {
              var pad = 4 - value.length;

              if (pad > 0) {
                value = value + '[0-9]{' + pad + '}';
              }
            } else {
              if (value.length === 1) {
                value = '0' + value;
              }
            }

            if (j <= 3) {
              dateParts.push(value);
            } else {
              timeParts.push(value);
            }
          }

          // ['DD', 'MM', 'YYYY'] to 'YYYY-MM-DD'
          var re = dateParts.reverse().join('-');

          if (timeParts.length) {
            re = re + 'T' + timeParts.join(':');
          }

          return re;
        }
      }

      return null;
    }

    return searchToDateRegExp;
  });
})();
