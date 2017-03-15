 $("#username").change(function () {
    var username = $(this).val();
    $.ajax({
        url: '/ajax/validate_username/',
        data: {
            'username': username
        },
        dataType: 'json',
        success: function (data) {
            if (data.is_taken) {
                $("#username").removeClass("valid");
                $("#username").addClass("invalid");
            }else{
                $("#username").removeClass("invalid");
                $("#username").addClass("valid");
            }
        }
    });
});

$("#password2").change(function(){
    var password = $("#password").val();
    var password2 = $(this).val();
    
    $.ajax({
        url: '/ajax/validate_password/',
        data: {
            'pass': password,
            'pass2':password2,
        },
        dataType: 'json',
        success: function (data) {
            if (!data.is_same) {
                $("#password").removeClass("valid");
                $("#password").addClass("invalid");
                $("#password2").removeClass("valid");
                $("#password2").addClass("invalid");
            }else{
                $("#password").removeClass("invalid");
                $("#password").addClass("valid");
                $("#password2").removeClass("invalid");
                $("#password2").addClass("valid");    
            }
        }
    });
});


$("#password").change(function(){
    var password = $(this).val();
    var password2 = $("#password2").val();
    
    $.ajax({
        url: '/ajax/validate_password/',
        data: {
            'pass': password,
            'pass2':password2,
        },
        dataType: 'json',
        success: function (data) {
            if (!data.is_same) {
                $("#password").removeClass("valid");
                $("#password").addClass("invalid");
                $("#password2").removeClass("valid");
                $("#password2").addClass("invalid");
            }else{
                $("#password").removeClass("invalid");
                $("#password").addClass("valid");
                $("#password2").removeClass("invalid");
                $("#password2").addClass("valid");    
            }
        }
    });
});
