$(document).ready(function () {
    if ($('#id_pay_date').val() != "") {
        flatpickr(
            '#id_pay_date',
            {
                dateFormat: "Y-m-d",
                disableMobile: "true"
            }
        );
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
                defaultDate: date_info.join('-'),
                dateFormat: "Y-m-d",
                disableMobile: "true"
            }
        );
    }
})