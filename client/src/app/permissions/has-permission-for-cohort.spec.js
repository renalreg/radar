(function() {
  'use strict';

  describe('hasPermissionForCohort', function() {
    beforeEach(module('radar'));

    var hasPermissionForCohort;
    var store;

    beforeEach(inject(function(_hasPermissionForCohort_, _store_) {
      hasPermissionForCohort = _hasPermissionForCohort_;
      store = _store_;
    }));

    it('denies when the user is not in the cohort', function() {
      var user = store.create('users', {});
      expect(hasPermissionForCohort(user, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user is in the cohort without the permission', function() {
      var cohort = store.create('cohort', {id: 1});
      var user = store.create('users', {cohorts: [
        {
          cohort: cohort,
          permissions: []
        }
      ]});
      expect(hasPermissionForCohort(user, cohort, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      expect(hasPermissionForCohort(user, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user is the cohort with the permission', function() {
      var cohort = store.create('cohort', {id: 1});
      var user = store.create('users', {cohorts: [
        {
          cohort: cohort,
          permissions: ['VIEW_PATIENT']
        }
      ]});
      expect(hasPermissionForCohort(user, cohort, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
