$(document).ready(function () {
   $('.bar-icon').click(function(){
       $('.sidebar').toggleClass('collapse-sidebar');
       $('.sidebar li span').toggle(100);
       $('.logo').toggleClass('adjust-size');
       $('.main').toggleClass('expand-nav');
       $('.bar-1').toggleClass('bar-1-active');
       $('.bar-2').toggleClass('bar-2-active');
       $('.bar-3').toggleClass('bar-3-active');
   });    
});

function edit(){
    $('.contact-details h5').css('border-bottom-color', '#e0e6e9');
    $('.about-me p').css('border-bottom-color' , '#e0e6e9');
    $('.contact-details h5').hover(function(){
        $(this).css('border-bottom-color' , '#719cca');
    });
    $('.contact-details h5').mouseout(function(){
        $(this).css('border-bottom-color', '#e0e6e9');
    });

    $('.about-me p').hover(function(){
        $(this).css('border-bottom-color' , '#719cca');
    });
    $('.about-me p').mouseout(function(){
        $(this).css('border-bottom-color', '#e0e6e9');
    });
}