// Code that executes on page load go in initializeAppSpecific()

"use strict"

function initializeAppSpecific() {
    var pts = []
    for (var i=0; i < flightPath.length; i++) {
        var steerPoint = flightPath[i]
        var pt = googLL(steerPoint)
        var identTxt = '<h3 style="background-color: yellow; opacity:0.8;">' + steerPoint[2] + '</h3>'
        new TxtOverlay(pt, identTxt, 'customBox', map)
        //drawLine take an arrow, not goog.maps.LatLng.
        pts.push([flightPath[i][0], flightPath[i][1]])
    }

    drawLine(pts, '#3333CC', 6, 0.8, false, map, false)

    for (var i=0; i < divertFields.length; i++) {
        var divert =  divertFields[i]
        var divertPt = googLL(divert)
        var path = 'M -22,15 0,-20 22,15 z'
        var divertTxt = '<h4 style="background-color: orange; opacity:0.8;">' + divert[2] + '</h4>'
        new TxtOverlay(divertPt, divertTxt, 'customBox', map)

        //todo different colors for military/civil fields. Ie black  vs blue
        drawMarker(divertPt, 0, '#000000', 2, 1.0, false, path, map, false)
    }


    //drawMarker(pos, hdg, color, weight, opacity, filled, path, map, draggable)

}