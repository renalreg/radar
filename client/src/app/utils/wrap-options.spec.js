(function() {
  'use strict';

  describe('wrap options', function() {
    beforeEach(module('radar'));

    describe('to radio view', function() {
      var toRadioView;

      beforeEach(inject(function(_toRadioView_) {
        toRadioView = _toRadioView_;
      }));

      it('handles a model object', function() {
        expect(toRadioView({id: 123})).toEqual(123);
      });

      it('handles a string', function() {
        expect(toRadioView('hello')).toEqual('hello');
      });
    });

    describe('to radio model', function() {
      var toRadioModel;

      beforeEach(inject(function(_toRadioModel_) {
        toRadioModel = _toRadioModel_;
      }));

      it('handles a model object', function() {
        expect(toRadioModel(
          [
            {
              id: 1,
              value: 'foo'
            },
            {
              id: 2,
              value: 'bar'
            },
            {
              id: 3,
              value: 'baz'
            }
          ],
          2
        )).toEqual({
          id: 2,
          value: 'bar'
        });
      });

      it('handles a string', function() {
        expect(toRadioModel(['foo', 'bar', 'baz'], 'bar')).toEqual('bar');
      });
    });

    describe('wrap radio options', function() {
      var wrapRadioOptions;

      beforeEach(inject(function(_wrapRadioOptions_) {
        wrapRadioOptions = _wrapRadioOptions_;
      }));

      it('handles an empty list', function() {
        expect(wrapRadioOptions([])).toEqual([]);
      });

      it('handles a list of strings', function() {
        expect(wrapRadioOptions(['foo', 'bar', 'baz'])).toEqual([
          {
            id: 'foo',
            label: 'foo'
          },
          {
            id: 'bar',
            label: 'bar'
          },
          {
            id: 'baz',
            label: 'baz'
          }
        ]);
      });

      it('handles a list of objects', function() {
        expect(wrapRadioOptions([
          {
            id: 1,
            label: 'foo'
          },
          {
            id: 2,
            label: 'bar'
          },
          {
            id: 3,
            label: 'baz'
          }
        ])).toEqual([
          {
            id: 1,
            label: 'foo'
          },
          {
            id: 2,
            label: 'bar'
          },
          {
            id: 3,
            label: 'baz'
          }
        ]);
      });
    });

    describe('to select view', function() {
      var toSelectView;

      beforeEach(inject(function(_toSelectView_) {
        toSelectView = _toSelectView_;
      }));

      it('handles null', function() {
        expect(toSelectView(null)).toBeNull();
      });

      it('handles undefined', function() {
        expect(toSelectView(undefined)).toBeNull();
      });

      it('handles a string', function() {
        expect(toSelectView('hello')).toEqual({
          id: 'hello',
          label: 'hello',
          value: 'hello'
        });
      });

      it('handles an object', function() {
        expect(toSelectView({
          id: 1,
          label: 'foo'
        })).toEqual({
          id: 1,
          label: 'foo',
          value: {
            id: 1,
            label: 'foo'
          }
        });
      });
    });

    describe('to select model', function() {
      var toSelectModel;

      beforeEach(inject(function(_toSelectModel_) {
        toSelectModel = _toSelectModel_;
      }));

      it('handles null', function() {
        expect(toSelectModel(null)).toBeNull();
      });

      it('handles undefined', function() {
        expect(toSelectModel(undefined)).toBeNull();
      });

      it('handles a object selection', function() {
        expect(toSelectModel({
          id: 1,
          label: 'foo',
          value: {
            id: 1,
            label: 'foo'
          }
        })).toEqual({
          id: 1,
          label: 'foo'
        });
      });

      it('handles a string selection', function() {
        expect(toSelectModel({
          id: 'foo',
          label: 'foo',
          value: 'foo'
        })).toEqual('foo');
      });
    });

    describe('wrap select options', function() {
      var wrapSelectOptions;

      beforeEach(inject(function(_wrapSelectOptions_) {
        wrapSelectOptions = _wrapSelectOptions_;
      }));

      it('handles an empty list', function() {
        expect(wrapSelectOptions([])).toEqual([]);
      });

      it('handles a list of strings', function() {
        expect(wrapSelectOptions(['foo', 'bar', 'baz'])).toEqual([
          {
            id: 'foo',
            label: 'foo',
            value: 'foo'
          },
          {
            id: 'bar',
            label: 'bar',
            value: 'bar'
          },
          {
            id: 'baz',
            label: 'baz',
            value: 'baz'
          }
        ]);
      });

      it('handles a list of objects', function() {
        expect(wrapSelectOptions([
          {
            id: 1,
            label: 'foo'
          },
          {
            id: 2,
            label: 'bar'
          },
          {
            id: 3,
            label: 'baz'
          }
        ])).toEqual([
          {
            id: 1,
            label: 'foo',
            value: {
              id: 1,
              label: 'foo'
            }
          },
          {
            id: 2,
            label: 'bar',
            value: {
              id: 2,
              label: 'bar'
            }
          },
          {
            id: 3,
            label: 'baz',
            value: {
              id: 3,
              label: 'baz'
            }
          }
        ]);
      });
    });
  });
})();
