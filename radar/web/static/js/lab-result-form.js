$(function() {
    $('#lab_group_definition_id').change(function() {
        var lab_group_definition_id = $(this).val();

        if (lab_group_definition_id) {
            $('#lab_group_form').html('<p><img src="/static/img/spinner.gif" /></p>');

            var lab_group_definition_id = $(this).val();
            var url = '../forms/' + lab_group_definition_id + '/';
            $.get(url, function(data) {
                $('#lab_group_form').html(data);
                init_datepickers();
            });
        } else {
            $('#lab_group_form').html('<p>Please choose a lab order above.</p>');
        }
    });
});