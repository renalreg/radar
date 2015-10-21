(function() {
  'use strict';

  var app = angular.module('radar.utils');

  app.factory('dateSearch', function() {
    // Date:
    // 9
    // 99
    // 99/
    // 99/9
    // 99/99
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

    var dateTimeRegExp = new RegExp(
      '^\\s*' +
      '(?:([0-9]{1,2})' + // begin day
      '(?:(/)' + // begin separator
      '(?:([0-9]{1,2})' + // begin month
      '(?:(/)' + // begin separator
      '(?:([0-9]{1,4})' + // begin year
      '(?:(\\s+)' + // begin separator
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
      ')?' + // end separator
      ')?' + // end year
      ')?' + // end separator
      ')?' + // end month
      ')?' + // end separator
      ')?' + // end day
      '\\s*$'
    );

    var timeRegExp = new RegExp(
      '^\\s*' +
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

    function _getDateRegExp(params) {
      var d = (
        getDigitGroupRegExp(params.year, 4) +
        '-' +
        getDigitGroupRegExp(params.month, 2) +
        '-' +
        getDigitGroupRegExp(params.day, 2)
      );

      var dt = (
        d +
        'T' +
        getDigitGroupRegExp(params.hour, 2) +
        ':' +
        getDigitGroupRegExp(params.minute, 2) +
        ':' +
        getDigitGroupRegExp(params.second, 2) +
        '(?:Z|[+-][0-9]{2}:[0-9]{2})?'
      );

      if (params.hour || params.minute || params.second) {
        return '(?:' + dt + ')';
      } else {
        return '(?:(?:' + d + ')|(?:' + dt + '))';
      }
    }

    function getDateRegExp(params) {
      var s;

      if (params.dayMonthSeparator || params.hourMinuteSeparator) {
        s = _getDateRegExp(params)
      } else {
        var value = params.day;

        s = (
          '(?:' +
          _getDateRegExp({year: value}) + '|' +
          _getDateRegExp({month: value}) + '|' +
          _getDateRegExp({day: value}) + '|' +
          _getDateRegExp({hour: value}) + '|' +
          _getDateRegExp({minute: value}) + '|' +
          _getDateRegExp({second: value}) +
          ')'
        )
      }

      s = '^' + s + '$';

      return new RegExp(s);
    }

    function getDigitGroupRegExp(digits, n) {
      var length = digits ? digits.length : 0;
      var pad = n - length;

      if (pad == n) {
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
      var params;
      var match;
      var f;

      if (match = dateTimeRegExp.exec(search)) {
        params = {
          day: match[1],
          dayMonthSeparator: match[2],
          month: match[3],
          monthYearSeparator: match[4],
          year: match[5],
          yearHourSeparator: match[6],
          hour: match[7],
          hourMinuteSeparator: match[8],
          minute: match[9],
          minuteSecondSeparator: match[10],
          second: match[11],
        };
      } else if (match = timeRegExp.exec(search)) {
        params = {
          hour: match[1],
          hourMinuteSeparator: match[2],
          minute: match[3],
          minuteSecondSeparator: match[4],
          second: match[5],
        };
      }

      if (match) {
        var regExp = getDateRegExp(params);

        f = function(value) {
          return regExp.test(value);
        }
      } else {
        f = function() {
          return false;
        }
      }

      return f;
    }

    return dateSearch;
  });
})();
