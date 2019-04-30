$(document).ready(function() {
    var table = $('#table').DataTable();
     
    $('#table tbody').on('click', 'tr', function () {
        $("#PatientsInfoModal").modal();
    } );
} );
