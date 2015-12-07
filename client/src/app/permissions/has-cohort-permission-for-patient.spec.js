(function() {
  'use strict';

  describe('hasCohortPermissionForPatient', function() {
    beforeEach(module('radar'));

    var hasCohortPermissionForPatient;
    var store;

    beforeEach(inject(function(_hasCohortPermissionForPatient_, _store_) {
      hasCohortPermissionForPatient = _hasCohortPermissionForPatient_;
      store = _store_;
    }));

    it('denies when the user and patient are in disjoint cohorts', function() {
      var cohort1 = store.create('cohorts', {id: 1});
      var cohort2 = store.create('cohorts', {id: 2});
      var user = store.create('users', {cohorts: [{cohort: cohort1, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {cohorts: [{cohort: cohort2}]});
      expect(hasCohortPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('denies when the user lacks the permission', function() {
      var cohort = store.create('cohorts', {id: 1});
      var user = store.create('users', {cohorts: [{cohort: cohort, permissions: []}]});
      var patient = store.create('patient', {cohorts: [{cohort: cohort}]});
      expect(hasCohortPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(false);
    });

    it('grants when the user is an admin', function() {
      var user = store.create('users', {isAdmin: true});
      var patient = store.create('patient', {});
      expect(hasCohortPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(true);
    });

    it('grants when the user has the permission', function() {
      var cohort = store.create('cohorts', {id: 1});
      var user = store.create('users', {cohorts: [{cohort: cohort, permissions: ['VIEW_PATIENT']}]});
      var patient = store.create('patient', {cohorts: [{cohort: cohort}]});
      expect(hasCohortPermissionForPatient(user, patient, 'VIEW_PATIENT')).toBe(true);
    });
  });
})();
