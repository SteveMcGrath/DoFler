image_ts = 0;
account_id = 0;

function ui_images(images_max) {
    $.getJSON('/get/reset/images', function(reset){
        if (reset){
            $('.dofler-img').remove();
        };
        $.getJSON('/get/images/' + image_ts, function(data){
            $.each(data, function(key, val){
                if ($('img[src="/get/image/' + val.md5sum + '"]').length < 1){
                    if (val.timestamp > image_ts ){
                        image_ts = val.timestamp;
                    };
                    if (!reset){
                        $('#images-display').prepend('<img class="dofler-img" src="/get/image/' + val.md5sum + '" />');
                        if ($('.dofler-img').length > images_max){
                            $('.dofler-img:last').remove();
                        };
                    };
                };
            });
        });
    });
};

function ui_accounts(accounts_max) {
    $.getJSON('/get/reset/accounts', function(reset){
        if (reset){
            $('.dofler-account').remove();
        };
        $.getJSON('/get/accounts/' + account_id, function(data){
            $.each(data, function(key, val){
                account_id = val.id;
                if (val.proto == 'ADMIN' && val.username == 'ADMIN' && val.password == 'ADMIN'){
                    $('#accounts-table tbody').prepend('<tr class="dofler-account">' +
                        '<td class="text" colspan="4">' + val.info + '</td>'
                    );
                }else{
                    $('#accounts-table tbody').prepend('<tr class="dofler-account">' + 
                        '<td class="text">' + val.info.substr(0,28) + '</td>' + 
                        '<td class="text">' + val.proto + '</td>' + 
                        '<td class="text">' + val.username.substr(0,15) + '</td>' + 
                        '<td class="text">' + val.password.substr(0,15) + '</td></tr>'
                    );
                };
                if ($('.dofler-account').length > accounts_max){
                    $('.dofler-account:last').remove();
                };
            });
        });
    });
};

function ui_stats(stats_max) {
    $.getJSON('/get/stats/' + stats_max, function(data){
        $.plot('#proto-trend', data, {xaxis: { mode: "time", position: "right", timezone: "browser"}, 
                legend: {position: "nw"}
            //legend: {container: $('#proto-legend')}
        });
    });
};

function ui_vulns(vulns_max){
    $.getJSON('/get/vulns/' + vulns_max, function(data){
        $('#vuln-table tbody').empty();
        max = data['vuln_max']
        $.each(data['hosts'], function(key, val){
            $('#vuln-table tbody').append('<tr><td class="text">' + val.host + '</td><td><div class="vulnerabilities">' + 
              '<div class="v-crit" style="width:' + ((val.critical / max * 100) - 0.1).toFixed(1) + '%;"></div>' +
              '<div class="v-high" style="width:' + ((val.high / max * 100) - 0.1).toFixed(1) + '%;"></div>' +
              '<div class="v-med" style="width:' + ((val.medium / max * 100) - 0.1).toFixed(1) + '%;"></div>' +
              '<div class="v-low" style="width:' + ((val.low / max * 100) - 0.1).toFixed(1) + '%;"></div>' +
              '<div class="v-info" style="width:' + ((val.info / max * 100) - 0.1).toFixed(1) + '%;"></div>' +
              '</div></td></tr>'
            );
        })
    })
}


$(function(){
    $.getJSON('/get/settings', function(settings){
        if (settings['stats_enabled']){
            ui_stats(settings['stats_max']);
            window.setInterval(ui_stats, settings['stats_delay'] * 1000);
        };
        if (settings['accounts_enabled']){
            ui_accounts(settings['accounts_max']);
            window.setInterval(ui_accounts, settings['accounts_delay'] * 1000);
        };
        if (settings['images_enabled']){
            ui_images(settings['images_max']);
            window.setInterval(ui_images, settings['images_delay'] * 1000);
        };
        if (settings['vulns_enabled']){
            ui_vulns(settings['vulns_max']);
            window.setInterval(ui_vulns, settings['vulns_delay'] * 1000);
        };
    });
});