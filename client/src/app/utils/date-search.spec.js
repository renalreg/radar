(function() {
  'use strict';

  describe('date search', function() {
    beforeEach(module('radar.utils'));

    var dateSearch;

    beforeEach(inject(function (_dateSearch_) {
      dateSearch = _dateSearch_;
    }));

    it('empty string', function () {
      var f = dateSearch('');

      expect(f('')).toBe(false);
      expect(f('hello')).toBe(false);
      expect(f('2015-01-02')).toBe(true);
    });

    it('[0-9]', function () {
      var f = dateSearch('1');

      expect(f('')).toBe(false);
      expect(f('hello')).toBe(false);
      expect(f('1')).toBe(false);

      expect(f('0003-00-00')).toBe(false);

      expect(f('1-00-00')).toBe(false);
      expect(f('10-00-00')).toBe(false);
      expect(f('100-00-00')).toBe(false);
      expect(f('1000-00-00')).toBe(true);
      expect(f('0100-00-00')).toBe(false);
      expect(f('0010-00-00')).toBe(false);
      expect(f('0001-00-00')).toBe(true);

      expect(f('0000-1-00')).toBe(false);
      expect(f('0000-10-00')).toBe(true);
      expect(f('0000-01-00')).toBe(true);

      expect(f('0000-00-1')).toBe(false);
      expect(f('0000-00-10')).toBe(true);
      expect(f('0000-00-01')).toBe(true);

      expect(f('0000-00-00T1:00:00')).toBe(false);
      expect(f('0000-00-00T10:00:00')).toBe(true);
      expect(f('0000-00-00T01:00:00')).toBe(true);

      expect(f('0000-00-00T00:1:00')).toBe(false);
      expect(f('0000-00-00T00:10:00')).toBe(true);
      expect(f('0000-00-00T00:01:00')).toBe(true);

      expect(f('0000-00-00T00:00:1')).toBe(false);
      expect(f('0000-00-00T00:00:10')).toBe(true);
      expect(f('0000-00-00T00:00:01')).toBe(true);
    });

    it('[0-9]{2}', function () {
      var f = dateSearch('12');

      expect(f('12-00-00')).toBe(false);
      expect(f('120-00-00')).toBe(false);
      expect(f('012-00-00')).toBe(false);
      expect(f('0012-00-00')).toBe(true);
      expect(f('1200-00-00')).toBe(true);

      expect(f('0000-12-00')).toBe(true);

      expect(f('0000-00-12')).toBe(true);

      expect(f('0000-00-00T12:00:00')).toBe(true);

      expect(f('0000-00-00T00:12:00')).toBe(true);

      expect(f('0000-00-00T00:00:12')).toBe(true);
    });

    it('[0-9]{2}/', function () {
      var f = dateSearch('12/');

      expect(f('12-00-00')).toBe(false);
      expect(f('120-00-00')).toBe(false);
      expect(f('012-00-00')).toBe(false);
      expect(f('0012-00-00')).toBe(false);
      expect(f('1200-00-00')).toBe(false);

      expect(f('0000-12-00')).toBe(false);

      expect(f('0000-00-12')).toBe(true);

      expect(f('0000-00-00T12:00:00')).toBe(false);

      expect(f('0000-00-00T00:12:00')).toBe(false);

      expect(f('0000-00-00T00:00:12')).toBe(false);
    });

    it('[0-9]{2}/[0-9]', function () {
      var f = dateSearch('12/1');

      expect(f('0012-01-00')).toBe(false);
      expect(f('1200-01-00')).toBe(false);
      expect(f('0012-10-00')).toBe(false);
      expect(f('1200-10-00')).toBe(false);

      expect(f('0000-12-01')).toBe(false);
      expect(f('0000-12-10')).toBe(false);

      expect(f('0000-01-12')).toBe(true);
      expect(f('0000-10-12')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}', function () {
      var f = dateSearch('12/10');

      expect(f('0012-10-00')).toBe(false);
      expect(f('1200-10-00')).toBe(false);

      expect(f('0000-12-10')).toBe(false);

      expect(f('0000-10-12')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/', function () {
      var f = dateSearch('12/10/');

      expect(f('0012-10-00')).toBe(false);
      expect(f('1200-10-00')).toBe(false);

      expect(f('0000-12-10')).toBe(false);

      expect(f('0000-10-12')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]', function () {
      var f = dateSearch('12/10/4');

      expect(f('4-10-12')).toBe(false);
      expect(f('40-10-12')).toBe(false);
      expect(f('400-10-12')).toBe(false);
      expect(f('4000-10-12')).toBe(true);
      expect(f('0400-10-12')).toBe(false);
      expect(f('0040-10-12')).toBe(false);
      expect(f('0004-10-12')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{2}', function () {
      var f = dateSearch('12/10/42');

      expect(f('42-10-12')).toBe(false);
      expect(f('420-10-12')).toBe(false);
      expect(f('4200-10-12')).toBe(true);
      expect(f('0420-10-12')).toBe(false);
      expect(f('0042-10-12')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{3}', function () {
      var f = dateSearch('12/10/999');

      expect(f('999-10-12')).toBe(false);
      expect(f('9990-10-12')).toBe(true);
      expect(f('0999-10-12')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{4}', function () {
      var f = dateSearch('12/10/2015');

      expect(f('2015-10-12')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]', function () {
      var f = dateSearch('12/10/2015 1');

      expect(f('2015-10-12T00:00:00')).toBe(false);
      expect(f('2015-10-12T01:00:00')).toBe(true);
      expect(f('2015-10-12T10:00:00')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}', function () {
      var f = dateSearch('12/10/2015 12');

      expect(f('2015-10-12T00:00:00')).toBe(false);
      expect(f('2015-10-12T12:00:00')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:', function () {
      var f = dateSearch('12/10/2015 12:');

      expect(f('2015-10-12T00:00:00')).toBe(false);
      expect(f('2015-10-12T12:00:00')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]', function () {
      var f = dateSearch('12/10/2015 12:3');

      expect(f('2015-10-12T12:00:00')).toBe(false);
      expect(f('2015-10-12T12:03:00')).toBe(true);
      expect(f('2015-10-12T12:30:00')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}', function () {
      var f = dateSearch('12/10/2015 12:34');

      expect(f('2015-10-12T12:00:00')).toBe(false);
      expect(f('2015-10-12T12:34:00')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:', function () {
      var f = dateSearch('12/10/2015 12:34:');

      expect(f('2015-10-12T12:00:00')).toBe(false);
      expect(f('2015-10-12T12:34:00')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]', function () {
      var f = dateSearch('12/10/2015 12:34:5');

      expect(f('2015-10-12T12:34:00')).toBe(false);
      expect(f('2015-10-12T12:34:50')).toBe(true);
      expect(f('2015-10-12T12:34:05')).toBe(true);
    });

    it('[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}', function () {
      var f = dateSearch('12/10/2015 12:34:56');

      expect(f('2015-10-12T12:34:00')).toBe(false);
      expect(f('2015-10-12T12:34:56')).toBe(true);
    });

    it('[0-9]{2}:', function () {
      var f = dateSearch('12:');

      expect(f('0000-00-00T00:00:00')).toBe(false);
      expect(f('1200-00-00T00:00:00')).toBe(false);
      expect(f('0012-00-00T00:00:00')).toBe(false);
      expect(f('0000-12-00T00:00:00')).toBe(false);
      expect(f('0000-00-12T00:00:00')).toBe(false);
      expect(f('0000-00-00T00:12:00')).toBe(false);
      expect(f('0000-00-00T00:00:12')).toBe(false);

      expect(f('0000-00-00T12:00:00')).toBe(true);
    });

    it('[0-9]{2}:[0-9]', function () {
      var f = dateSearch('12:3');

      expect(f('0000-00-00T00:00:00')).toBe(false);
      expect(f('0000-00-00T12:30:00')).toBe(true);
      expect(f('0000-00-00T12:03:00')).toBe(true);
    });

    it('[0-9]{2}:[0-9]{2}', function () {
      var f = dateSearch('12:34');

      expect(f('0000-00-00T00:00:00')).toBe(false);
      expect(f('0000-00-00T12:34:00')).toBe(true);
    });

    it('[0-9]{2}:[0-9]{2}:', function () {
      var f = dateSearch('12:34:');

      expect(f('0000-00-00T00:00:00')).toBe(false);
      expect(f('0000-00-00T12:34:00')).toBe(true);
    });

    it('[0-9]{2}:[0-9]{2}:[0-9]', function () {
      var f = dateSearch('12:34:5');

      expect(f('0000-00-00T00:00:00')).toBe(false);
      expect(f('0000-00-00T12:34:50')).toBe(true);
      expect(f('0000-00-00T12:34:05')).toBe(true);
    });

    it('[0-9]{2}:[0-9]{2}:[0-9]{2}', function () {
      var f = dateSearch('12:34:56');

      expect(f('0000-00-00T00:00:00')).toBe(false);
      expect(f('0000-00-00T12:34:56')).toBe(true);
    });

    it('trailing whitespace', function () {
      var f = dateSearch('   12/10/2015 12:34:56  ');

      expect(f('2015-10-12T12:34:00')).toBe(false);
      expect(f('2015-10-12T12:34:56')).toBe(true);
    });
  });
})();
