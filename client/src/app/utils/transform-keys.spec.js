// jshint camelcase: false
// jscs:disable requireCamelCaseOrUpperCaseIdentifiers

(function() {
  'use strict';

  describe('camel case keys', function() {
    beforeEach(module('radar.utils'));

    var camelCaseKeys;

    beforeEach(inject(function(_camelCaseKeys_) {
      camelCaseKeys = _camelCaseKeys_;
    }));

    it('handles an empty object', function() {
      expect(camelCaseKeys({})).toEqual({});
    });

    it('handles an empty list', function() {
      expect(camelCaseKeys([])).toEqual([]);
    });

    it('handles a flat object', function() {
      expect(camelCaseKeys({
        key_one: 'key_one',
        key_two: 'key_two'
      })).toEqual({
        keyOne: 'key_one',
        keyTwo: 'key_two'
      });
    });

    it('handles nested objects', function() {
      expect(camelCaseKeys({
        key_one: {
          key_one_one: 'value_one_one',
          key_one_two: 'value_one_two'
        },
        key_two: {
          key_two_one: 'value_two_one',
          key_two_two: 'value_two_two'
        }
      })).toEqual({
        keyOne: {
          keyOneOne: 'value_one_one',
          keyOneTwo: 'value_one_two'
        },
        keyTwo: {
          keyTwoOne: 'value_two_one',
          keyTwoTwo: 'value_two_two'
        }
      });
    });

    it('handles a list of objects', function() {
      expect(camelCaseKeys([
        {
          item_one_key_one: 'item_one_value_one',
          item_one_key_two: 'item_one_value_two'
        },
        {
          item_two_key_one: 'item_two_value_one',
          item_two_key_two: 'item_two_value_two'
        }
      ])).toEqual([
        {
          itemOneKeyOne: 'item_one_value_one',
          itemOneKeyTwo: 'item_one_value_two'
        },
        {
          itemTwoKeyOne: 'item_two_value_one',
          itemTwoKeyTwo: 'item_two_value_two'
        }
      ]);
    });

    it('skips constants', function() {
      expect(camelCaseKeys({
        KEY_1: 'value_1',
        KEY_2: 'value_2'
      })).toEqual({
        KEY_1: 'value_1',
        KEY_2: 'value_2'
      });
    });
  });

  describe('snake case keys', function() {
    beforeEach(module('radar'));

    var snakeCaseKeys;

    beforeEach(inject(function(_snakeCaseKeys_) {
      snakeCaseKeys = _snakeCaseKeys_;
    }));

    it('handles an empty object', function() {
      expect(snakeCaseKeys({})).toEqual({});
    });

    it('handles an empty list', function() {
      expect(snakeCaseKeys([])).toEqual([]);
    });

    it('handles a flat object', function() {
      expect(snakeCaseKeys({
        keyOne: 'keyOne',
        keyTwo: 'keyTwo'
      })).toEqual({
        key_one: 'keyOne',
        key_two: 'keyTwo'
      });
    });

    it('handles nested objects', function() {
      expect(snakeCaseKeys({
        keyOne: {
          keyOneOne: 'valueOneOne',
          keyOneTwo: 'valueOneTwo'
        },
        keyTwo: {
          keyTwoOne: 'valueTwoOne',
          keyTwoTwo: 'valueTwoTwo'
        }
      })).toEqual({
        key_one: {
          key_one_one: 'valueOneOne',
          key_one_two: 'valueOneTwo'
        },
        key_two: {
          key_two_one: 'valueTwoOne',
          key_two_two: 'valueTwoTwo'
        }
      });
    });

    it('handles a list of objects', function() {
      expect(snakeCaseKeys([
        {
          itemOneKeyOne: 'itemOneValueOne',
          itemOneKeyTwo: 'itemOneValueTwo'
        },
        {
          itemTwoKeyOne: 'itemTwoValueOne',
          itemTwoKeyTwo: 'itemTwoValueTwo'
        }
      ])).toEqual([
        {
          item_one_key_one: 'itemOneValueOne',
          item_one_key_two: 'itemOneValueTwo'
        },
        {
          item_two_key_one: 'itemTwoValueOne',
          item_two_key_two: 'itemTwoValueTwo'
        }
      ]);
    });

    it('skips constants', function() {
      expect(snakeCaseKeys({
        KEY1: 'value1',
        KEY2: 'value2'
      })).toEqual({
        KEY1: 'value1',
        KEY2: 'value2'
      });
    });
  });
})();
