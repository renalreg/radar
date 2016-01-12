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

    it('denies when the user doesn\'t belong to a group with the permission', function() {
      var group = store.create('groups', {id: 1});
      var user = store.create('users', {groups: [
        {
          group: group,
          permissions: []
        }
      ]});
      expect(hasPermissionForAnyGroup(user, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      expect(hasPermissionForAnyGroup(user, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user belongs to a group with the permission', function() {
      var group = store.create('groups', {id: 1});
      var user = store.create('users', {groups: [
        {
          group: group,
          permissions: ['VIEW_PATIENT']
        }
      ]});
      expect(hasPermissionForAnyGroup(user, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
