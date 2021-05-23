let today = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());
$(document).ready(function () {
    $('#div_id_departure_time input').removeClass('gj-textbox-md')
    $('#div_id_arrival_time input').removeClass('gj-textbox-md')
    $('#id_destination_time_zone').prepend('<option value="" selected></option>')
})
$('#id_departure_time').datetimepicker({
    footer: true,
    modal: true,
    datepicker: {
        minDate: today,
        showRightIcon: false,
    },
    format: 'dd/mm/yyyy HH:MM'
});
$('#id_arrival_time').datetimepicker({
    footer: true,
    modal: true,
    datepicker: {
        minDate: today,
        showRightIcon: false,
    },
    format: 'dd/mm/yyyy HH:MM'
});
$("#id_dearture_time, #id_arrival_time").keydown(function (e) {
    e.preventDefault();
});