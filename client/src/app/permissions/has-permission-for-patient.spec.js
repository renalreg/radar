(function() {
  'use strict';

  describe('hasPermissionForPatient', function() {
    beforeEach(module('radar'));

    var hasPermissionForPatient;
    var store;

    beforeEach(inject(function(_hasPermissionForPatient_, _store_) {
      hasPermissionForPatient = _hasPermissionForPatient_;
      store = _store_;
    }));

    it('denies when the user and patient are in disjoint groups', function() {
      var group1 = store.create('groups', {id: 1});
      var group2 = store.create('groups', {id: 2});
      var user = store.create('users', {groups: [{group: group1, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {groups: [{group: group2}]});
      expect(hasPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user lacks the permission', function() {
      var group = store.create('groups', {id: 1});
      var user = store.create('users', {groups: [{group: group, permissions: []}]});
      var patient = store.create('patient', {groups: [{group: group}]});
      expect(hasPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      var patient = store.create('patient', {});
      expect(hasPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user has the permission', function() {
      var group = store.create('groups', {id: 1});
      var user = store.create('users', {groups: [{group: group, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {groups: [{group: group}]});
      expect(hasPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
