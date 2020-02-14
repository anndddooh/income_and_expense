$(document).ready(function () {
    const config = {
        defaultDate: this_year + "-" + this_mon + "-1"
    }
    flatpickr('#id_pay_date', config);
});