(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('dateSearch', function() {
    // Date:
    // 9
    // 99
    // 99/
    // 99/9
    // 99/99/
    // 99/99/9
    // 99/99/99
    // 99/99/999
    // 99/99/9999

    // Date and time:
    // 99/99/9999 9
    // 99/99/9999 99
    // 99/99/9999 99:
    // 99/99/9999 99:9
    // 99/99/9999 99:99
    // 99/99/9999 99:99:
    // 99/99/9999 99:99:9
    // 99/99/9999 99:99:99

    // Time:
    // 9
    // 99
    // 99:
    // 99:9
    // 99:99
    // 99:99:
    // 99:99:9
    // 99:99:99

    var searchRegExp = new RegExp(
      '^\\s*' +
      '(?:([0-9]{1,2})' + // begin day
      '(?:(/)' + // begin separator
      '(?:([0-9]{1,2})' + // begin month
      '(?:(/)' + // begin separator
      '(?:([0-9]{1,4})' + // begin year
      '(?:(\\s+)' + // begin separator
      ')?' + // end separator
      ')?' + // end year
      ')?' + // end separator
      ')?' + // end month
      ')?' + // end separator
      ')?' + // end day
      '(?:([0-9]{1,2})' + // begin hour
      '(?:(:)' + // begin separator
      '(?:([0-9]{1,2})' + // begin minute
      '(?:(:)' + // begin separator
      '(?:([0-9]{1,2})' + // begin second
      ')?' + // end second
      ')?' + // end separator
      ')?' + // end minute
      ')?' + // end separator
      ')?' + // end hour
      '\\s*$'
    );

    function _getDateRegExp(year, month, day, hour, minute, second) {
      var d = (
        getDigitGroupRegExp(year, 4) +
        '-' +
        getDigitGroupRegExp(month, 2) +
        '-' +
        getDigitGroupRegExp(day, 2)
      );

      var dt = (
        d +
        'T' +
        getDigitGroupRegExp(hour, 2) +
        ':' +
        getDigitGroupRegExp(minute, 2) +
        ':' +
        getDigitGroupRegExp(second, 2) +
        '(?:Z|[+-][0-9]{2}:[0-9]{2})?'
      );

      if (hour) {
        return '(?:' + dt + ')';
      } else {
        return '(?:(?:' + d + ')|(?:' + dt + '))';
      }
    }

    function getDateRegExp(match) {
      var day = match[1] || '';
      var dayMonthSeparator = match[2];
      var month = match[3] || '';
      var year = match[5] || '';
      var hour = match[7] || '';
      var minute = match[9] || '';
      var second = match[11] || '';

      var s;

      if (!dayMonthSeparator) {
        s = (
          '(?:' +
          _getDateRegExp(day, '', '', '', '', '') + '|' +
          _getDateRegExp('', day, '', '', '', '') + '|' +
          _getDateRegExp('', '', day, '', '', '') + '|' +
          _getDateRegExp('', '', '', day, '', '') + '|' +
          _getDateRegExp('', '', '', '', day, '') + '|' +
          _getDateRegExp('', '', '', '', '', day) +
          ')'
        )
      } else {
        s = _getDateRegExp(year, month, day, hour, minute, second)
      }

      s = '^' + s + '$';

      return new RegExp(s);
    }

    function getDigitGroupRegExp(digits, width) {
      var pad = width - digits.length;

      if (pad == width) {
        return '[0-9]{' + pad + '}';
      } else if (pad > 0) {
        return (
          '(?:' +
          '[0-9]{' + pad + '}' + digits +
          '|' +
          digits + '[0-9]{' + pad + '}' +
          ')'
        );
      } else {
        return digits;
      }
    }

    function dateSearch(search) {
      var match = searchRegExp.exec(search);

      if (match === null) {
        return function() {
          return false;
        }
      } else {
        var valueRegExp = getDateRegExp(match);

        return function(value) {
          return valueRegExp.test(value);
        }
      }
    }

    return dateSearch;
  });
})();
