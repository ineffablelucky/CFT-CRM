$(document).ready(function () {
   $('.bar-icon').click(function(){
       $('.sidebar').toggleClass('collapse-sidebar');
       $('.sidebar li span').toggle(100);
       $('.logo').toggleClass('adjust-size');
       $('.main').toggleClass('expand-nav');
       $('.bar-1-active').toggleClass('bar-1');
       $('.bar-2-active').toggleClass('bar-2');
       $('.bar-3-active').toggleClass('bar-3');
   });  
});