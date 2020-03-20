$(document).ready(function () {
    $("#nav-item-method-require").addClass("active");

    $("#done-modal").on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        $(this).find('.modal-body p strong').text(button.data('name'))
        $(this).find('form').attr('action', button.data('url'))
    })
});