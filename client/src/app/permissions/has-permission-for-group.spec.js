(function() {
  'use strict';

  describe('hasPermissionForGroup', function() {
    beforeEach(module('radar'));

    var hasPermissionForGroup;
    var store;

    beforeEach(inject(function(_hasPermissionForGroup_, _store_) {
      hasPermissionForGroup = _hasPermissionForGroup_;
      store = _store_;
    }));

    it('denies when the user is not in the group', function() {
      var user = store.create('users', {});
      expect(hasPermissionForGroup(user, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user is in the group without the permission', function() {
      var group = store.create('groups', {id: 1});
      var user = store.create('users', {groups: [
        {
          group: group,
          permissions: []
        }
      ]});
      expect(hasPermissionForGroup(user, group, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      expect(hasPermissionForGroup(user, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user is the group with the permission', function() {
      var group = store.create('groups', {id: 1});
      var user = store.create('users', {groups: [
        {
          group: group,
          permissions: ['VIEW_PATIENT']
        }
      ]});
      expect(hasPermissionForGroup(user, group, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
