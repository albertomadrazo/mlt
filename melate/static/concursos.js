$(function(){
    var moveLeft = 20; 
    var moveDown = 10;

    // $('.pelota').on('mouseover', function(){
    // });

    $('.pelota').hover(function(event){
        var numero = $(this).text();
        var numeroOver = $(this).find('span').html();
        var ocurrencias = $.get('numero', {n:numeroOver}).done(function(data){
            $('.num-stats-cont').show();
            $('.num-stats-cont div:first-of-type').html(numero);
            $('.ocurrencias').html(data);

            console.log('---> ' + data);
        });
        

    }, function(){
        $('.num-stats-cont').hide();
    });

    $('.pelota').mousemove(function(event){
        $('.num-stats-cont').css({'top':event.pageY + moveDown, 'left':event.pageX + moveLeft});
    });
});