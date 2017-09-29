$(function(){
    var moveLeft = 20; 
    var moveDown = 10;

    $('.pelota').hover(function(event){
        var numero = $(this).text();
        var numeroOver = $(this).find('span').html();
        var ocurrencias = $.get('numero', {n:numeroOver}).done(function(data){
            console.log(data);
            var resultados = data;
            console.log('res: '+ resultados);
            $('.num-stats-cont').show();
            $('.num-stats-cont div:first-of-type').html(numero);
            $('.total-ocurrencias').html(resultados.total_ocurrencias);
            $('.ocurrencias-natural').html(resultados.ocurrencias_natural);
            $('.ocurrencias-adicional').html(resultados.ocurrencias_adicional);
        });
    }, function(){ $('.num-stats-cont').hide(); });

    $('.pelota').mousemove(function(event){
        $('.num-stats-cont').css({'top':event.pageY + moveDown, 'left':event.pageX + moveLeft});
    });
});