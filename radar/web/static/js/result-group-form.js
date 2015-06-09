$(function() {
    $('#result_group_definition_id').change(function() {
        var result_group_definition_id = $(this).val();

        if (result_group_definition_id) {
            $('#result_group_form').html('<p><img src="/static/img/spinner.gif" /></p>');
            var url = '../forms/' + result_group_definition_id + '/';
            $.get(url, function(data) {
                $('#result_group_form').html(data);
                init_datepickers();
            });
        } else {
            $('#result_group_form').html('<p>Please choose a result group above.</p>');
        }
    });
});
