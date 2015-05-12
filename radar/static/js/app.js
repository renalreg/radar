$(function() {
    $('.datepicker').each(function () {
        var options = {};

        var dateFormat = $(this).attr('data-date-format');

        if (dateFormat !== undefined) {
            options['dateFormat'] = dateFormat;
        }

        $(this).datepicker(options);
    });

    $('.chosen-select').chosen();
});

function toggle_extra_fields(input_name, extra_selector, value) {
    $('input[name=' + input_name + '], select[name=' + input_name + ']').change(function() {
        var input_type = $(this).attr('type')

        function show() {
            $(extra_selector).show();
        }

        function hide() {
            $(extra_selector).hide();
        }

        if (input_type == 'radio') {
            // This radio button is checked
            if ($(this).prop('checked')) {
                // The value matches the desired value
                if ($(this).val() == value) {
                    show();
                } else {
                    hide();
                }
            } else if ($('input[name=' + input_name + ']:checked').val() === undefined) {
                // No radio buttons selected, so hide
                hide();
            }
        } else if (input_type == 'checkbox') {
            var checked = $(this).is(':checked')

            if (value == 'y') {
                if (checked) {
                    show();
                } else {
                    hide();
                }
            } else if (value == 'n') {
                if (checked) {
                    hide();
                } else {
                    show();
                }
            }
        } else {
            if ($(this).val() == value) {
                show();
            } else {
                hide();
            }
        }
    }).trigger('change');
}