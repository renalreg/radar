(function() {
  'use strict';

  describe('hasOrganisationPermissionForPatient', function() {
    beforeEach(module('radar'));

    var hasOrganisationPermissionForPatient;
    var store;

    beforeEach(inject(function(_hasOrganisationPermissionForPatient_, _store_) {
      hasOrganisationPermissionForPatient = _hasOrganisationPermissionForPatient_;
      store = _store_;
    }));

    it('denies when the user and patient are in disjoint organisations', function() {
      var organisation1 = store.create('organisations', {id: 1});
      var organisation2 = store.create('organisations', {id: 2});
      var user = store.create('users', {organisations: [{organisation: organisation1, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {organisations: [{organisation: organisation2}]});
      expect(hasOrganisationPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user lacks the permission', function() {
      var organisation = store.create('organisations', {id: 1});
      var user = store.create('users', {organisations: [{organisation: organisation, permissions: []}]});
      var patient = store.create('patient', {organisations: [{organisation: organisation}]});
      expect(hasOrganisationPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      var patient = store.create('patient', {});
      expect(hasOrganisationPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user has the permission', function() {
      var organisation = store.create('organisations', {id: 1});
      var user = store.create('users', {organisations: [{organisation: organisation, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {organisations: [{organisation: organisation}]});
      expect(hasOrganisationPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
