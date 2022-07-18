$(document).ready(function () {
    $("#nav-item-loan").addClass("active");

    $(".delete-button").each(function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    });

    $(".update-loan").each(function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    });
});