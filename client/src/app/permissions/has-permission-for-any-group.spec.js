(function() {
  'use strict';

  describe('hasPermissionForAnyCohort', function() {
    beforeEach(module('radar'));

    var hasPermissionForAnyCohort;
    var store;

    beforeEach(inject(function(_hasPermissionForAnyCohort_, _store_) {
      hasPermissionForAnyCohort = _hasPermissionForAnyCohort_;
      store = _store_;
    }));

    it('denies when the user doesn\'t belong to a cohort with the permission', function() {
      var cohort = store.create('cohort', {id: 1});
      var user = store.create('users', {cohorts: [
        {
          cohort: cohort,
          permissions: []
        }
      ]});
      expect(hasPermissionForAnyCohort(user, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      expect(hasPermissionForAnyCohort(user, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user belongs to a cohort with the permission', function() {
      var cohort = store.create('cohort', {id: 1});
      var user = store.create('users', {cohorts: [
        {
          cohort: cohort,
          permissions: ['VIEW_PATIENT']
        }
      ]});
      expect(hasPermissionForAnyCohort(user, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
