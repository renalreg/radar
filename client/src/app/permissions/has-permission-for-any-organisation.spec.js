(function() {
  'use strict';

  describe('hasPermissionForAnyOrganisation', function() {
    beforeEach(module('radar'));

    var hasPermissionForAnyOrganisation;
    var store;

    beforeEach(inject(function(_hasPermissionForAnyOrganisation_, _store_) {
      hasPermissionForAnyOrganisation = _hasPermissionForAnyOrganisation_;
      store = _store_;
    }));

    it('denies when the user doesn\'t belong to an organisation with the permission', function() {
      var organisation = store.create('organisation', {id: 1});
      var user = store.create('users', {organisations: [
        {
          organisation: organisation,
          permissions: []
        }
      ]});
      expect(hasPermissionForAnyOrganisation(user, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      expect(hasPermissionForAnyOrganisation(user, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user belongs to an organisation with the permission', function() {
      var organisation = store.create('organisation', {id: 1});
      var user = store.create('users', {organisations: [
        {
          organisation: organisation,
          permissions: ['VIEW_PATIENT']
        }
      ]});
      expect(hasPermissionForAnyOrganisation(user, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
