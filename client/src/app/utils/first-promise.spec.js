(function() {
  'use strict';

  describe('first promise', function() {
    beforeEach(module('radar.utils'));

    var firstPromise;
    var $q;
    var $rootScope;

    beforeEach(inject(function(_firstPromise_, _$q_, _$rootScope_) {
      firstPromise = _firstPromise_;
      $q = _$q_;
      $rootScope = _$rootScope_;
    }));

    it('handles an empty list', function() {
      var originalValue = {};
      var resolvedValue = originalValue;

      firstPromise([]).then(function(value) {
        resolvedValue = value;
      });

      expect(resolvedValue).toEqual(originalValue);
      $rootScope.$apply();
      expect(resolvedValue).toBeUndefined();
    });

    it('handles one promise', function() {
      var originalValue = {};
      var resolvedValue = originalValue;
      var deferred = $q.defer();

      firstPromise([deferred.promise]).then(function(value) {
        resolvedValue = value;
      });

      expect(resolvedValue).toEqual(originalValue);
      $rootScope.$apply();
      expect(resolvedValue).toEqual(originalValue);
      deferred.resolve(42);
      expect(resolvedValue).toEqual(originalValue);
      $rootScope.$apply();
      expect(resolvedValue).toBe(42);
    });

    it('handles multiple promises', function() {
      var originalValue = {};
      var resolvedValue = originalValue;
      var deferred1 = $q.defer();
      var deferred2 = $q.defer();

      firstPromise([deferred1.promise, deferred2.promise]).then(function(value) {
        resolvedValue = value;
      });

      expect(resolvedValue).toEqual(originalValue);
      $rootScope.$apply();
      expect(resolvedValue).toEqual(originalValue);
      deferred1.resolve(123);
      expect(resolvedValue).toEqual(originalValue);
      $rootScope.$apply();
      expect(resolvedValue).toEqual(originalValue);
      deferred2.resolve(456);
      expect(resolvedValue).toEqual(originalValue);
      $rootScope.$apply();
      expect(resolvedValue).toBe(123);
    });
  });
})();
