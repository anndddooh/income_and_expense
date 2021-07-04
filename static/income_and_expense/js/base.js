$(document).ready(function () {
    var nav_item_date = $('#nav-item-date');
    var this_year = nav_item_date.data('year');
    var this_mon = nav_item_date.data('mon');
    $('#current_month').val(this_year + '-' + to_double_digits(this_mon));

    $('#current_month').change(function () {
        var year_and_mon = $('#current_month').val().split('-');
        var path_name = $('#current_month').data('path-name');
        var url = '/income_and_expense/move_another_page' + '?path_name=' + path_name + '&year=' + year_and_mon[0] + '&month=' + year_and_mon[1];
        location.href = url;
    })
});