$(document).on('submit', '#reset-form', function(e){
    e.preventDefault();
    $.ajax({
        type:'POST',
        url:'/forgot-password/',
        data:$(this).serialize(),
        success:function(data){
            if(data.success == 'true'){
                alert("Password reset instructions have been mailed to you");
                window.location = '/login/';
            }
            else{

                alert("Email address not registered!");
            }
        }
     });
});
