function get_year_and_mon_after_x_mon(year, mon, x) {
    var year_and_mon = {}
    var date = new Date();

    date.setFullYear(year);
    date.setMonth(mon - 1);

    date.setMonth(date.getMonth() + x);

    year_and_mon['year'] = date.getFullYear();
    year_and_mon['mon'] = date.getMonth() + 1;

    return year_and_mon;
}

$(document).ready(function set_nav_item_date() {
    var nav_item_date = $('#nav-item-date');
    var this_year = nav_item_date.data('year');
    var this_mon = nav_item_date.data('mon');
    var disp_mon_deltas = [-3, -2, -1, 1, 2, 3];

    $.each(disp_mon_deltas, function(index, mon_delta) {
        var year_and_mon = get_year_and_mon_after_x_mon(this_year, this_mon, mon_delta);
        var year = year_and_mon['year'];
        var mon = year_and_mon['mon'];
        var id = '#nav-item-date-' + (index + 1);
        var url = $(id).attr('href');

        $(id).text(year + '年' + mon + '月');
        $(id).attr('href', url + year + '/' + mon + '/income');
    })
});