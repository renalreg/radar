(function() {
  'use strict';

  describe('hasGroupPermissionForPatient', function() {
    beforeEach(module('radar'));

    var hasGroupPermissionForPatient;
    var store;

    beforeEach(inject(function(_hasGroupPermissionForPatient_, _store_) {
      hasGroupPermissionForPatient = _hasGroupPermissionForPatient_;
      store = _store_;
    }));

    it('denies when the user and patient are in disjoint cohorts', function() {
      var cohort1 = store.create('cohorts', {id: 1});
      var cohort2 = store.create('cohorts', {id: 2});
      var user = store.create('users', {cohorts: [{cohort: cohort1, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {cohorts: [{cohort: cohort2}]});
      expect(hasGroupPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user and patient are in disjoint organisations', function() {
      var organisation1 = store.create('organisations', {id: 1});
      var organisation2 = store.create('organisations', {id: 2});
      var user = store.create('users', {organisations: [{organisation: organisation1, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {organisations: [{organisation: organisation2}]});
      expect(hasGroupPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user lacks the cohort permission', function() {
      var cohort = store.create('cohorts', {id: 1});
      var user = store.create('users', {cohorts: [{cohort: cohort, permissions: []}]});
      var patient = store.create('patient', {cohorts: [{cohort: cohort}]});
      expect(hasGroupPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user lacks the organisation permission', function() {
      var organisation = store.create('organisations', {id: 1});
      var user = store.create('users', {organisations: [{organisation: organisation, permissions: []}]});
      var patient = store.create('patient', {organisations: [{organisation: organisation}]});
      expect(hasGroupPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      var patient = store.create('patient', {});
      expect(hasGroupPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user has the permission through a cohort', function() {
      var cohort = store.create('cohorts', {id: 1});
      var user = store.create('users', {cohorts: [{cohort: cohort, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {cohorts: [{cohort: cohort}]});
      expect(hasGroupPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user has the permission through an organisation', function() {
      var organisation = store.create('organisations', {id: 1});
      var user = store.create('users', {organisations: [{organisation: organisation, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {organisations: [{organisation: organisation}]});
      expect(hasGroupPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
