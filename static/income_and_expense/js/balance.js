$(document).ready(function () {
    $("#nav-item-balance").addClass("active");

    $(".update-balance").each(function () {
        $(this).modalForm({ formURL: $(this).data('url') });
    });
});