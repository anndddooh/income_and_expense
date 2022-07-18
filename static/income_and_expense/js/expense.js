$(document).ready(function () {
    $("#nav-item-expense").addClass("active");

    $(".delete-button").each(function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    });

    $(".update-exp").each(function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    });
});