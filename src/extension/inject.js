 var lastComponentView;
 $(window).bind('hashchange', function(data) {
        var url = data.originalEvent.newURL;
        var components = URLToArray(url);
        if(components.view == "SpotDetail"){
            var spotID = components.spotID;
            setTimeout(function(){
                if( !$(".spotdetail .contents ul.list").children().last().hasClass("nextSpot") ){
                    $(".spotdetail .contents ul.list").append("<li class=\"listitem nextSpot\"> <a class=\"title\" data-href=\"type=list&amp;login_required=false&amp;spotID="+spotID+"&amp;channel=spots&amp;view=NextSpots\" onclick=\"app.navigate('type=list&amp;login_required=false&amp;spotID="+spotID+"&amp;channel=spots&amp;view=NextSpots'); return false;\"> <span class=\"icon\"> <img src=\"http://vdnkr.be/icon-next.png\" alt=\"nextUp\"> </span> <div class=\"vertically-centered has-description\"> <h1>What's up next?</h1> <p>Find out what to do next!</p> </div> </a> </li>");
                }
            }, 1000);
       }
       if(components.view == "NextSpots" && lastComponentView == "SpotDetail"){
            var spotID = components.spotID;
            setTimeout(function(){
               /*     <div class=\"listitem more\">
                        <a class=\"morebutton color-f01558\" data-href=\"params%5Bchannel%5D=shoppingplaces&amp;type=list&amp;channel=builtin&amp;view=Discover\" onclick=\"app.navigate('params%5Bchannel%5D=shoppingplaces&amp;type=list&amp;channel=builtin&amp;view=Discover'); return false;\">
                            <img src=\"https://vikingspots.com/s/v-186ca808//citylife/img/icons/white/shopping.png\" class=\"icon\" alt=\"shopping\"></a><a class=\"title\" data-href=\"params%5Bid%5D=10784&amp;type=spotdetail&amp;channel=spots&amp;view=SpotDetail\" onclick=\"app.navigate('params%5Bid%5D=10784&amp;type=spotdetail&amp;channel=spots&amp;view=SpotDetail'); return false;\">
                            <div class=\"vertically-centered has-description\">
                                <h1>Wheels and more</h1>
                                <p>1km — Banden Eric</p>
                            </div>
                        </a>
                    </div> */
                $("header .navigation .title").html("What's up Next?");
               whatsUpNext(spotID);
            }, 1500);
       }
       lastComponentView = components.view;
});


function URLToArray(url) {
  var request = {};
  var pairs = url.substring(url.indexOf('#') + 1).split('&');
  for (var i = 0; i < pairs.length; i++) {
    var pair = pairs[i].split('=');
    if (i==0){
        request["spotID"] = decodeURIComponent(pair[1]);
    }else{
        request[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
    }
  }
  return request;
}

function whatsUpNext(spotID){
    $(".page.list .contents").html("");
    
    function main () {
        window.postMessage({ type: "FROM_PAGE", token: config.token }, "*");
        console.log("page token: "+event.data.token);
    }
    var script = document.createElement('script');
    script.appendChild(document.createTextNode('('+ main +')();'));
    (document.body || document.head || document.documentElement).appendChild(script);
    
    window.addEventListener("message", function(event) {
        // We only accept messages from ourselves
        if (event.source != window)
          return;

        if (event.data.type && (event.data.type == "FROM_PAGE")) {
            console.log("script token: "+event.data.token);
            requestJson(event.data.token, spotID);
        }
    }, false);
}

function requestJson(token, spotID){
    var whatsNextUrl="http://linseysAPI.be/api/"+token+"/whatsnext/"+spotID+"/"
    window.alert(whatsNextUrl);
    /*$.getJSON( whatsNextUrl, function(data) {
        $.each(data, function(key, val) {
        });
    });*/
    for(var i=0;i<5;i++){
        var html;
        html = "<div class=\"listitem more\">";
        html += "<a class=\"morebutton color-f01558\" data-href=\"params%5Bchannel%5D=shoppingplaces&amp;type=list&amp;channel=builtin&amp;view=Discover\" onclick=\"app.navigate('params%5Bchannel%5D=shoppingplaces&amp;type=list&amp;channel=builtin&amp;view=Discover'); return false;\">";
        html += "<img src=\"https://vikingspots.com/s/v-186ca808//citylife/img/icons/white/shopping.png\" class=\"icon\" alt=\"shopping\"></a><a class=\"title\" data-href=\"params%5Bid%5D=10784&amp;type=spotdetail&amp;channel=spots&amp;view=SpotDetail\" onclick=\"app.navigate('params%5Bid%5D=10784&amp;type=spotdetail&amp;channel=spots&amp;view=SpotDetail'); return false;\">";
        html += "<div class=\"vertically-centered has-description\">";
        html += "<h1>"+spotID+"</h1>";
        html += "<p>1km — Banden Eric</p>";
        html += "</div>";
        html += "</a>";
        html += "</div>";
        $(".page.list .contents").append(html);
    }
}
