$(document).ready(function(){

    // Initiate all of the configuration variables that we will be using.
    urlhost = '';
    var reset_accounts = false;
    var reset_images = false;
    var reset_stats = false;
    var max_images = 200;
    var max_accounts = 25;
    var max_stats = 10;
    var account_id = 0;
    var image_ts = 0;


    function reset_content(){
        $.getJSON(urlhost + '/resets', function(data){
            if(data.hasOwnProperty('images')){
                reset_images = true;
                $('.dofler-img').remove();
            } else {
                reset_images = false;
            };

            if(data.hasOwnProperty('stats')){
                reset_stats = true;
                $('.dofler-stat').remove();
            } else {
                reset_stats = false;
            };

            if(data.hasOwnProperty('accounts')){
                reset_accounts = true;
                $('.dofler-account').remove();
            } else {
                reset_accounts = false;
            };
        });
    };


    function images(){
        $.getJSON(urlhost + '/images/' + image_ts, function(data){
            $.each(data, function(key, val){
                image_ts = val.timestamp;
                if(!reset_images){
                    $("#images").prepend('<img class="dofler-img" src="' 
                                         + urlhost + '/image/' + val.md5 + '" />');
                    if($('.dofler-img').length > max_images){
                        $('.dofler-img:last').remove();
                    };
                };
            });
        });
    };


    function stats(){
        //Nothing Here Yet
    };

    function accounts(){
        $.getJSON(urlhost + '/accounts/' + account_id, function(data){
            $.each(data, function(key, val){
                account_id = val.id;
                if(!reset_accounts){
                    $("#accounts-table tbody").prepend('<tr class="dofler-account">' +
                        '<td>' + val.info.substr(0,28) + '</td>' +
                        '<td>' + val.proto + '</td>' +
                        '<td>' + val.username + '</td>' +
                        '<td>' + val.password.substr(0,15) + '</td></tr>'
                    );
                    if($('.dofler-account').length > max_accounts){
                        $('.dofler-account:last').remove();
                    };
                };
            });
        });
        $.get(urlhost + '/account_total', function(data){
            $("#accounts-total").empty().append('<i><b>Total : </b>' + data + '</i>');
        });
    };

    window.setInterval(reset_content, 5000);
    $.getJSON(urlhost + '/config', function(data){
        if(data.accounts){
            document.getElementById('accounts').style.display = 'block';
            window.setInterval(accounts, (data.account_delay * 1000));
        };
        if(data.stats){
            document.getElementById('stats').style.display = 'block';
            window.setInterval(stats, (data.stats_delay * 1000));
        };
        if(data.images){
            document.getElementById('images').style.display = 'block';
            window.setInterval(images, (data.image_delay * 1000));
        };
    });
});