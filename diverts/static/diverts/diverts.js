// Code that executes on page load go in initializeAppSpecific()

"use strict"

function initializeAppSpecific() {
    var pts = []
    for (var i=0; i < flightPath.length; i++) {
        var pt = new google.maps.LatLng(flightPath[i][0], flightPath[i][1])
        var identTxt = '<h3 style="background-color: yellow; opacity:0.8;">' + flightPath[i][2] + '</h3>'
        var identLabel = new TxtOverlay(pt, identTxt, 'customBox', map)
    }
    console.log("TEST")

    drawLine(pts, '#FF0000', 8, 0.6, false, map)

//    makePath(pts, false)

}