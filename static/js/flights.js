let today = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());
$(document).ready(function () {
    $('#id_departure_time').parent().addClass('input-group')
    $('#div_id_departure_time span').css('position', 'initial')
    $('#div_id_departure_time input').removeClass('gj-textbox-md')
    $('#id_arrival_time').parent().addClass('input-group')
    $('#div_id_arrival_time span').css('position', 'initial')
    $('#div_id_arrival_time input').removeClass('gj-textbox-md')
    $('#div_id_baggage .mb-3').addClass('input-group').append('<span class="input-group-text font-weight-bold">KG</span>')
})
$('#id_departure_time').datetimepicker({
    footer: true,
    modal: true,
    datepicker: {
        minDate: today,
        icons: { rightIcon: '<span class="input-group-text role=right-icon" role="right-icon"><i class="fas fa-calendar-alt"></i></span>' },
    },
    format: 'dd/mm/yyyy hh:mm'
});
$('#id_arrival_time').datetimepicker({
    footer: true,
    modal: true,
    datepicker: {
        minDate: today,
        icons: { rightIcon: '<span class="input-group-text role=right-icon" role="right-icon"><i class="fas fa-calendar-alt"></i></span>' },
    },
    format: 'dd/mm/yyyy hh:mm'
});