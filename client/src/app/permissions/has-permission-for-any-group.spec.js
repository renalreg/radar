(function() {
  'use strict';

  describe('hasPermissionForAnyGroup', function() {
    beforeEach(module('radar'));

    var hasPermissionForAnyGroup;
    var store;

    beforeEach(inject(function(_hasPermissionForAnyGroup_, _store_) {
      hasPermissionForAnyGroup = _hasPermissionForAnyGroup_;
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
      expect(hasPermissionForAnyGroup(user, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user doesn\'t belong to an organisation with the permission', function() {
      var organisation = store.create('organisation', {id: 1});
      var user = store.create('users', {organisations: [
        {
          organisation: organisation,
          permissions: []
        }
      ]});
      expect(hasPermissionForAnyGroup(user, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      expect(hasPermissionForAnyGroup(user, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user belongs to a cohort with the permission', function() {
      var cohort = store.create('cohort', {id: 1});
      var user = store.create('users', {cohorts: [
        {
          cohort: cohort,
          permissions: ['VIEW_PATIENT']
        }
      ]});
      expect(hasPermissionForAnyGroup(user, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user belongs to an organisation with the permission', function() {
      var organisation = store.create('organisation', {id: 1});
      var user = store.create('users', {organisations: [
        {
          organisation: organisation,
          permissions: ['VIEW_PATIENT']
        }
      ]});
      expect(hasPermissionForAnyGroup(user, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
