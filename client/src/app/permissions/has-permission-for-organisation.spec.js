(function() {
  'use strict';

  describe('hasPermissionForOrganisation', function() {
    beforeEach(module('radar'));

    var hasPermissionForOrganisation;
    var store;

    beforeEach(inject(function(_hasPermissionForOrganisation_, _store_) {
      hasPermissionForOrganisation = _hasPermissionForOrganisation_;
      store = _store_;
    }));

    it('denies when the user is not in the organisation', function() {
      var user = store.create('users', {});
      expect(hasPermissionForOrganisation(user, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user is in the organisation without the permission', function() {
      var organisation = store.create('organisation', {id: 1});
      var user = store.create('users', {organisations: [
        {
          organisation: organisation,
          permissions: []
        }
      ]});
      expect(hasPermissionForOrganisation(user, organisation, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      expect(hasPermissionForOrganisation(user, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user is the organisation with the permission', function() {
      var organisation = store.create('organisation', {id: 1});
      var user = store.create('users', {organisations: [
        {
          organisation: organisation,
          permissions: ['VIEW_PATIENT']
        }
      ]});
      expect(hasPermissionForOrganisation(user, organisation, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
