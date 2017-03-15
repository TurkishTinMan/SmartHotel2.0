$("#fine-1").change(function () {
    validate_period($(this),2);
});


function validate_period(currdate,num){
    currdate.unbind("change");
    var data_end = currdate.val();
    console.log(data_end);
    var dataToAppend ='<div><label>Periodo '+num+':</label><input type="text" name="periodo-'+num+'"></div><div><label>Fine:</label><input type="date" name="fine-'+num+'" id="fine-'+num+'"></div>'

    $.ajax({
        url: '/ajax/validate_period/',
        data: {
            'fine': data_end,
            'num':num,
        },
        dataType: 'json',
        success: function (data) {
            if(data.end){
                $("<button class='btn waves-effect waves-light btn-large' type='submit' name='action'>SALVA<i class='material-icons right'>done</i></button>").appendTo("#formper");
            }else{
                $(dataToAppend).appendTo("#formper");
                $("#fine-"+num).change(function () {
                    validate_period($(this),num+1);
                });
                
                $('#fine-'+num).pickadate({
                    selectMonths: true,
                    selectYears:false,
                    format:'dd/mm',
                    min:new Date(2017,parseInt(currdate.val()[3].concat(currdate.val()[4]))-1,currdate.val()[0].concat(currdate.val()[1])),
                    max:new Date(2017,11,31)
              });
            }
        }
    });
}
 