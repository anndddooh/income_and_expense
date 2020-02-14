$(document).ready(function () {
	$("#nav-item-income").addClass("active");

    $(".delete-button").each(function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    })

    $(".update-inc").on('click', function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    });
});