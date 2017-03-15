var count = 1;

$("#addType").click(function () {
    count++;
    var dataToAppend ='<div><label>Tipo '+count+':</label><input type="text" name="name-'+count+'"></div></div>'
    $(dataToAppend).appendTo("#formtyp");
});