

$(document).ready(function (){
//Funcionalidad para ocultar o visualizar vendedors y empresas

$("#id_solicitante").prop("readonly", true);


$("#div_vendedor").removeAttr('pk').hide();  
$("#div_proveedor").removeAttr('pk').hide();  


var borrado=0;

$("#id_tipo_solicitante").change(function () {
    var selected_option = $('#id_tipo_solicitante').val();

    if (selected_option === '0') {
        $('#div_vendedor').attr('pk','1').show();   
        $("#div_proveedor").removeAttr('pk').hide();  

    }
    if (selected_option == '1') {
      $("#div_vendedor").removeAttr('pk').hide();  
      $('#div_proveedor').attr('pk','1').show();   
    }
  })


$("#id_vendedor").change(function () { 
    $("#id_solicitante").val($('#div_vendedor').find(":selected").text());
})


$("#div_proveedor").change(function () { 
  $("#id_solicitante").val($('#div_proveedor').find(":selected").text());
})


});

