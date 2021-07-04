$(document).ready(function () {
    if ($('#id_pay_date').val() != "") {
        flatpickr('#id_pay_date');
    } else {
        flatpickr('#id_pay_date', {defaultDate: [new Date()]});
    }
})