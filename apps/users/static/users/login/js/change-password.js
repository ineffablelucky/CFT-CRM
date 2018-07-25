var app1 = document.getElementById('app1');
var app2 = document.getElementById('app2');
var app3 = document.getElementById('app3');
var app4 = document.getElementById('app4');

var typewriter1 = new Typewriter(app1, {
    loop: false,
    cursor:"",
    typingSpeed: 40,
    animateCursor: false
});

var typewriter2 = new Typewriter(app2, {
    loop: false,
    cursor:"",
    typingSpeed: 40,
    animateCursor: false
});

var typewriter3 = new Typewriter(app3, {
    loop: false,
    cursor:"",
    typingSpeed: 40,
    animateCursor: false
});

var typewriter4 = new Typewriter(app4, {
    loop: false,
    cursor:"",
    typingSpeed: 40,
    animateCursor: false
});



typewriter1.typeString('Stay connected to employees, anytime & anywhere')
.start();

typewriter2.typeString('Keep a track record of your work & schedule')
.pauseFor(1500)
.start();

typewriter3.typeString('Get access to employees\' corner, 24X7')
.start();

typewriter4.typeString('Time sheets saved for whenever you need them')
.start();


$(document).ready(function(){
    $('span').on("click",function(){
        if($(this).prev().attr("type") == "password"){
            $(this).removeClass("animation");
            $(this).prev().attr("type" , "text");
        }else{
            $(this).prev().attr("type" , "password");
            $(this).toggleClass("animation");
        }   
    });

    $('.token').hide();
    var token = $('.token');
    $('#change-password').submit(function(e){
        e.preventDefault();
        console.log(token.html());
        $.ajax({
            type:'POST',
            url:'/reset-password/'+token.html()+'/',

            data:$(this).serialize(),
            success:function(data){
                if(data.success == 'true'){
                    alert("Password has been changed successfully!");
                    window.location = '/';
                }
                else{
                    $('.error').empty();
                    for(var i=0;i<data.error.password2.length;i++){
                        $('.error').append('<li>'+data.error.password2[i]+ '</li>');
                    }
                }
            },
        });
    });
});




