$('.menu').each(function(index) {
    $(this).after('menu-index',index);
}).click(function(){
    var index = $(this).attr('menu-index');
    $('.menu[menu-index='+index+']').addClass('clicked_menu');
    $('.menu[menu-index='+index+']').removeClass('clicked_menu');
});
var index= $(this).attr('menu-index');