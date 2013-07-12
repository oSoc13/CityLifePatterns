/***
 * Copyright: OKFN Belgium
 * Authors: Linsey Raymaekers & Wouter vandenneucker
 * 
 * Comments:
 * If this page looks like a mess, it's because it is!
 * Some hackerish stuff is going on, but I'll explain it ;)
 * 
 */

var lastComponentView; //What kind of page did you view previously?
var userToken = ""; //keep the userToken available any time

//Whenever the anchor/hash of your URL changes:
$(window).bind('hashchange', function (data) {
    var url = data.originalEvent.newURL; //Store the old URL
    var components = URLToArray(url); //convert it to an array
    
    //If you're watching a SpotDetail page, add a button underneath it
    if (components.view == "SpotDetail") {
        var spotID = components.spotID;
        
        //but only after a timeout, because else it will be still looking at the previous page
        setTimeout(function () {
            //Don't add the button if the last button already is the nextSpot button (happens when you visit the same spot multiple times)
            if (!$(".spotdetail .contents ul.list").children().last().hasClass("nextSpot")) {
                $(".spotdetail .contents ul.list").append("<li class=\"listitem nextSpot\"> <a class=\"title\" data-href=\"type=list&amp;login_required=false&amp;spotID=" + spotID + "&amp;channel=spots&amp;view=NextSpots\" onclick=\"app.navigate('type=list&amp;login_required=false&amp;spotID=" + spotID + "&amp;channel=spots&amp;view=NextSpots'); return false;\"> <span class=\"icon\"> <img src=\"http://vdnkr.be/icon-next.png\" alt=\"nextUp\"> </span> <div class=\"vertically-centered has-description\"> <h1>What's up next?</h1> <p>Find out what to do next!</p> </div> </a> </li>");
            }
        }, 1000);
    }
    
    
    //When you go to a NextSpots view, you'll end up on a page saying that The makes didn't create that kind of page yet.
    //Yet we made that page, and we go to this error page to have the fancy page slide animation.
    
    //If you're watching the NextSpots view, and your last one was a SpotDetail, change the error-content
    if (components.view == "NextSpots" && lastComponentView == "SpotDetail") {
        var spotID = components.spotID;
        
        // Change the title from "Error" to "What's up Next?" and include the list of possible next spots.
        // But only after a timeout, because else it will be still looking at the previous page
        setTimeout(function () {
            $("header .navigation .title").html("What's up Next?");
            whatsUpNext(spotID); //This function renders and places the HTML Content of the Spots / Buttons
        }, 1500);
    }
    
    
    //Since we have glitches when we watch more than one "NextSpots" pages:
    //Whenever our last view was the "NextSpots" view, clear that view.
    //No timeout required, else we'd be clearing the wrong view.
    if (lastComponentView == "NextSpots") {
        $(".page.list .contents").html("");
    }
    
    //When the hash has changed and has been acted upon,
    //change the last view to the current view.
    lastComponentView = components.view;
});

//The URLToArray function converts the URL anchor / hash / URI to an array and returns it.
function URLToArray(url) {
    var request = {};
    var pairs = url.substring(url.indexOf('#') + 1).split('&'); //Pairs is an array of the components of an URI. In "http://yoursite.domain/#foo=bar&foolsbar=7" both "foo=bar" and "foolsbar=7" will be pairs
    
    //for every pair, match the key to the value
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i].split('='); //pair is an array: in "foo=bar" pair[0]=foo and pair[1]=bar
        
        //Just map the key to pair[0] and the value to pair[1]
        //except when your key would be "params[id]", javascript can't handle the [] when it isn't in an array. In that case, make the key "spotID".
        if (pair.indexOf("params[id]") != -1) {
            request["spotID"] = decodeURIComponent(pair[1]);
        } else {
            request[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
        }
    }
    return request;
}

//The whatsUpNext function renders and triggers the function to substitude the HTML content on the Error page
function whatsUpNext(spotID) {
    $(".page.list .contents").html(""); //Clear the Error page so the user won't get confused
    
    //If userToken is filled in already, request the Json with the valid next spots and render it's HTML
    if (userToken != "") {
        requestJson(userToken, spotID);
    }
    //If you don't have the token, better make sure we get it!
    else {
        //Here the true hackerish code starts, it's nasty, but the only way to let a page talk to a sandboxed extension on chrome.
        
        //this is the function "main()", we're not triggering it in this inject.js script.
        //Instead we're going to actually make a DOM element on the page itself, trigger it there and make it talk to us
        function main() {
            //window.postMessage is a part of the chrome API, it allows the window/page to broadcast a message in thin air.
            window.postMessage({
                type: "FROM_PAGE",
                token: config.token
            }, "*");
        }
        
        //So this is the part where we inject the function main() from above in the actual page/window
        var script = document.createElement('script');
        script.appendChild(document.createTextNode('(' + main + ')();'));
        (document.body || document.head || document.documentElement).appendChild(script);

        //Now the script is injected, and it will broadcast a message. So we better make sure we're listening.
        window.addEventListener("message", function (event) {
            //We only accept messages from ourselves, not from any other alien lifeform
            if (event.source != window)
                return;

            //When our script is talking, get the userToken (which is already defined on top) and request the Json with the valid next spots and render it's HTML
            if (event.data.type && (event.data.type == "FROM_PAGE")) {
                userToken = event.data.token;
                requestJson(userToken, spotID);
            }
        }, false);
    }

}


//After whatsUpNext has made sure we've got the userToken and the spotID, we request the next spots from our Django API
//For now, that Django instance runs locally (hence the 127.0.0.1 url)
function requestJson(token, spotID) {
    var whatsNextUrl = "http://127.0.0.1:8000/api/" + token + "/whatsnext/" + spotID + "/";
    
    //Request a json response from the above url and on succes, handle upon it.
    $.ajax({
        dataType: "json",
        url: whatsNextUrl,
        success: handleResponse
    });

    //The real fun part, actually make a button for every spot in the json
    function handleResponse(data) {
        theSpots = data.response.spots; //Cut things short, use theSpots instead of data.response.spots #lazy
        var html = ""; //init an emty html var and make it contain "". Not defining it upfront or defining it empty will make your code glitch.
        for (var i = 0; i < theSpots.length; i++) {
            //For every spot in the theSpots Array, parse the html and append it to the existing html var.
            html += "<div class=\"listitem more\">";
            html += "<a class=\"morebutton color-39c3ae\" data-href=\"params%5Bchannel%5D=shoppingplaces&amp;type=list&amp;channel=builtin&amp;view=Discover\" onclick=\"app.navigate('params%5Bchannel%5D=shoppingplaces&amp;type=list&amp;channel=builtin&amp;view=Discover'); return false;\">";
            html += "<img src=\"http://vdnkr.be/icon-next-white.png\" class=\"icon\" alt=\"shopping\"></a><a class=\"title\" data-href=\"params%5Bid%5D=" + theSpots[i].id + "&amp;type=spotdetail&amp;channel=spots&amp;view=SpotDetail\" onclick=\"app.navigate('params%5Bid%5D=" + theSpots[i].id + "&amp;type=spotdetail&amp;channel=spots&amp;view=SpotDetail'); return false;\">";
            html += "<div class=\"vertically-centered has-description\">";
            html += "<h1>" + theSpots[i].name + "</h1>";
            html += "<p>" + theSpots[i].description + "</p>";
            html += "</div>";
            html += "</a>";
            html += "</div>";
        }
        //When all spots are parsed, insert them on the former error page.
        $(".page.list .contents").html(html);
    }
}
