$(document).ready(function () {
	$("#nav-item-income").addClass("active");

    $(".delete-button").each(function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    });

    $(".update-inc").each(function () {
        $(this).modalForm({
            formURL: $(this).data('url')
        });
    });
});