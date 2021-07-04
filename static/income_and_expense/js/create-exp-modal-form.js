$(document).ready(function () {
    if ($('#id_pay_date').val() != "") {
        flatpickr('#id_pay_date', {dateFormat: "Y/m/d"});
    } else {
        current_date = new Date();
        date_info = [
            current_date.getFullYear(),
            to_double_digits(current_date.getMonth() + 1),
            to_double_digits(current_date.getDate())
        ];
        flatpickr(
            '#id_pay_date',
            {
                defaultDate: date_info.join('/'),
                dateFormat: "Y/m/d"
            }
        );
    }

    var template_exps = JSON.parse(document.getElementById('template-exps').textContent);

    $('#expense_type').change(function () {
        var val = $(this).val();

        if (val > 0) {
            var template_exp = template_exps[val - 1];

            $('#id_name').val(template_exp['name']);
            $('#id_pay_date').val(template_exp['pay_date']);
            $('#id_method option').filter(function(index) {
                return $(this).text() === template_exp['method'];
            }).prop('selected', true);
            if (template_exp['undecided'] === 'True') {
                $('#id_undecided').prop("checked", true);
            } else {
                $('#id_undecided').prop("checked", false);
            }
            if (template_exp['done'] === 'True') {
                $('#id_done').prop("checked", true);
            } else {
                $('#id_done').prop("checked", false);
            }
        }
    });
});