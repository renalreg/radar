(function() {
  'use strict';

  describe('any value', function() {
    beforeEach(module('radar'));

    var anyValue;

    beforeEach(inject(function (_anyValue_) {
      anyValue = _anyValue_;
    }));

    function matcher(x) {
      return x === 'hello';
    }

    it('match input', function () {
      expect(anyValue('hello', matcher)).toBe(true);
    });

    it('match in list', function () {
      expect(anyValue(['hello', 'world'], matcher)).toBe(true);
    });

    it('no match in list', function () {
      expect(anyValue(['foo', 'bar'], matcher)).toBe(false);
    });

    it('match in object value', function () {
      expect(anyValue({foo: 'hello'}, matcher)).toBe(true);
    });

    it('no match in object value', function () {
      expect(anyValue({foo: 'world'}, matcher)).toBe(false);
    });

    it('match in nested lists', function () {
      expect(anyValue(['foo', ['hello', 'world']], matcher)).toBe(true);
    });

    it('match in nested objects', function () {
      expect(anyValue({foo: {bar: 'hello'}}, matcher)).toBe(true);
    });

    it('match in list in object', function () {
      expect(anyValue({foo: ['hello', 'world']}, matcher)).toBe(true);
    });

    it('should not match keys', function () {
      expect(anyValue({hello: 'world'}, matcher)).toBe(false);
    });
  });
})();
