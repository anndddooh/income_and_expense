$(document).ready(function () {
    $("#nav-item-balance").addClass("active");

    $(".update-balance").on('click', function () {
        $(this).modalForm({ formURL: $(this).data('url') });
    });
});