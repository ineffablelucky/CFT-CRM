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

function addTask(){
    var value = $('#add-task').val();
    if($('#add-task').val() != "" ){
        $('.todo-container').append('<div class="row todo"><div class="col-lg-12 task-container"><label for="5">' + value + '<input type="checkbox" value="5" class="form-check-input" id="5"><span class="checkmark"></span></label></div></div>') 
        $('#add-task').val("");
    }
}

var input = document.getElementById("add-task");
input.addEventListener("keyup", function(event) {
    // event.preventDefault();
    if (event.keyCode === 13) {
        document.getElementsByClassName("add-btn")[0].click();
    }
});