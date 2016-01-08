(function() {
  'use strict';

  describe('store', function() {
    beforeEach(module('radar'));

    var store;
    var Model;

    beforeEach(inject(function(_store_, _Model_) {
      store = _store_;
      Model = _Model_;
    }));

    it('detects changes', function() {
      var x = store.pushToStore(new Model('foo', {
        id: 1,
        name: 'Foo'
      }));

      expect(x.isPristine()).toBe(true);
      expect(store.isPristine(x)).toBe(true);

      expect(x.isDirty()).toBe(false);
      expect(store.isDirty(x)).toBe(false);

      x.name = 'Bar';

      expect(x.isPristine()).toBe(false);
      expect(store.isPristine(x)).toBe(false);

      expect(x.isDirty()).toBe(true);
      expect(store.isDirty(x)).toBe(true);

      store.pushToStore(x);

      expect(x.isPristine()).toBe(true);
      expect(store.isPristine(x)).toBe(true);

      expect(x.isDirty()).toBe(false);
      expect(store.isDirty(x)).toBe(false);
    });
  });
})();
