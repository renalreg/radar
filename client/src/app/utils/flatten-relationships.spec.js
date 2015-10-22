(function() {
  'use strict';

  describe('flatten relationships', function() {
    beforeEach(module('radar'));

    var flattenRelationships;

    beforeEach(inject(function(_flattenRelationships_){
      flattenRelationships = _flattenRelationships_;
    }));

    it('handles an empty object', function() {
      expect(flattenRelationships({})).toEqual({});
    });

    it('handles an empty list', function() {
      expect(flattenRelationships([])).toEqual([]);
    });

    it('does nothing at the top level', function() {
      expect(flattenRelationships({
        id: 123,
        foo: 'bar'
      })).toEqual({
        id: 123,
        foo: 'bar'
      });
    });

    it('flattens child objects', function() {
      expect(flattenRelationships({
        id: 123,
        foo: {
          id: 456,
          hello: 'world'
        }
      })).toEqual({
        id: 123,
        foo: 456
      });
    });

    it('flattens grandchild objects', function() {
      expect(flattenRelationships({
        id: 123,
        foo: {
          hello: 'world',
          bar: {
            id: 789,
            hello: 'world'
          }
        }
      })).toEqual({
        id: 123,
        foo: {
          hello: 'world',
          bar: 789
        }
      });
    });

    it('flattens child objects with child objects', function() {
      expect(flattenRelationships({
        id: 123,
        foo: {
          id: 456,
          bar: {
            id: 789,
            hello: 'world'
          }
        }
      })).toEqual({
        id: 123,
        foo: 456
      });
    });

    it('flattens child lists', function() {
      expect(flattenRelationships({
        id: 123,
        foo: [
          {
            id: 1,
            hello: 'world'
          },
          {
            id: 2,
            hello: 'world'
          },
          {
            id:3,
            hello: 'world'
          }
        ]
      })).toEqual({
        id: 123,
        foo: [1, 2, 3]
      });
    });

    it('flattens child objects in lists', function() {
      expect(flattenRelationships({
        id: 123,
        foo: [
          {
            bar: {
              id: 123,
              hello: 'world'
            }
          },
          {
            bar: {
              id: 456,
              hello: 'world'
            }
          },
          {
            bar: {
              id: 789,
              hello: 'world'
            }
          }
        ]
      })).toEqual({
        id: 123,
        foo: [
          {
            bar: 123
          },
          {
            bar: 456
          },
          {
            bar: 789
          }
        ]
      });
    });
  });
})();
