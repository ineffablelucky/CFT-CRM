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