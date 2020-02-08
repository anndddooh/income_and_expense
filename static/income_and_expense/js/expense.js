$(document).ready(function () {
    $("#nav-item-expense").addClass("active");

    $(".delete-exp").each(function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    })

    $(".update-exp").on('click', function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    });
});