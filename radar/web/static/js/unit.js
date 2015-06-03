$(function() {
    load_recruitment_graph('recruitment.json', 'new_patients', 'New Patients by Month');
    load_recruitment_graph('recruitment.json?cumulative=1', 'total_patients', 'Total Patients by Month');
});
