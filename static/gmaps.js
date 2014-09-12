// Contains functions useful for general drawing on the Google Maps v3 API.

"use strict"

var map
var elevator


function initialize() {
    var mapOptions = {
        center: center,
        zoom: zoom,
        scaleControl: true,
        mapTypeId: mapTypeId,
        disableDefaultUI: true,
        disableDoubleClickZoom: true,
        draggableCursor:'crosshair'
    }
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions)
    elevator = new google.maps.ElevationService()
}


function googLL(coords) {
    // Return a gmaps LatLng object from a [lat, lon] array.
    return new google.maps.LatLng(coords[0], coords[1])
}


function moveLabel(marker, label) {
    google.maps.event.addListener(marker, 'dragend', function() {
        label.pos = marker.getPosition()
        label.draw()
    })
}


function moveLabelLine(line, label) {
    google.maps.event.addListener(line, 'dragend', function() {
        label.pos = line.getPath().getArray()[0]
        label.draw()
    })
}


function makePath(pts, close) {
if(typeof(close)==='undefined') close = false;
    var path = []
    for (var i in pts) {
        var pt = new google.maps.LatLng(pts[i][0], pts[i][1])
        path.push(pt)
    }
    if (close === true){
        path.push(new google.maps.LatLng(pts[0][0], pts[0][1]))
    }
    return path
}


function drawLine(pts, color, weight, opacity, close, map, draggable) {
    if(typeof(draggable)==='undefined')draggable = true
    return new google.maps.Polyline({
        path: makePath(pts, close),
        geodesic: true,
        strokeColor: color,
        strokeOpacity: opacity,
        strokeWeight: weight,
        draggable: draggable,
        map: map
    })
}


function drawPolygon(pts, color, weight, opacity, f_color, f_opacity, map) {
    return new google.maps.Polygon({
        path: makePath(pts),
        geodesic: true,
        strokeColor: color,
        strokeOpacity: opacity,
        strokeWeight: weight,
        fillColor: f_color,
        fillOpacity: f_opacity,
        draggable:true,
        map: map
    })
}


function drawMarker(pos, hdg, color, weight, opacity, filled, path, map, draggable) {
    // pos is a goog LL, which differs from the behavior of functions using makePath().
    if(typeof(draggable)==='undefined')draggable = true
    var fillOpacity = 0
    if (filled === true)fillOpacity = 1

    var Icon = {
        path: path,
        strokeColor: color,
        strokeWeight: weight,
        strokeOpacity: opacity,
        fillColor: color,
        fillOpacity: fillOpacity,
        rotation: hdg
    }

    return new google.maps.Marker({
        position: pos,
        icon: Icon,
        map: map,
        draggable: draggable
    })
}


// TxtOverlay adapded from this example:
// http://code.google.com/apis/maps/documentation/javascript/overlays.html#CustomOverlays
//text overlays
function TxtOverlay(pos, txt, cls, map){
    // Now initialize all properties.
    this.pos = pos;
    this.txt_ = txt;
    this.cls_ = cls;
    this.map_ = map;

    // We define a property to hold the image's
    // div. We'll actually create this div
    // upon receipt of the add() method so we'll
    // leave it null for now.
    this.div_ = null;

    // Explicitly call setMap() on this overlay
    this.setMap(map);
}

TxtOverlay.prototype = new google.maps.OverlayView();

TxtOverlay.prototype.onAdd = function(){
    // Note: an overlay's receipt of onAdd() indicates that
    // the map's panes are now available for attaching
    // the overlay to the map via the DOM.

    // Create the DIV and set some basic attributes.
    var div = document.createElement('DIV');
    div.className = this.cls_;
    div.innerHTML = this.txt_;

    // Set the overlay's div_ property to this DIV
    this.div_ = div;
    var overlayProjection = this.getProjection();
    var position = overlayProjection.fromLatLngToDivPixel(this.pos);
    div.style.left = position.x + 'px';
    div.style.top = position.y + 'px';
    // We add an overlay to a map via one of the map's panes.

    var panes = this.getPanes();
    panes.floatPane.appendChild(div);
}

TxtOverlay.prototype.draw = function(){
    var overlayProjection = this.getProjection();

    // Retrieve the southwest and northeast coordinates of this overlay
    // in latlngs and convert them to pixels coordinates.
    // We'll use these coordinates to resize the DIV.
    var position = overlayProjection.fromLatLngToDivPixel(this.pos);

    var div = this.div_;
    div.style.left = position.x + 'px';
    div.style.top = position.y + 'px';
}

//Optional: helper methods for removing and toggling the text overlay.
TxtOverlay.prototype.onRemove = function(){
    this.div_.parentNode.removeChild(this.div_);
    this.div_ = null;
}

TxtOverlay.prototype.hide = function(){
    if (this.div_) {
        this.div_.style.visibility = "hidden";
    }
}

TxtOverlay.prototype.show = function(){
    if (this.div_) {
        this.div_.style.visibility = "visible";
    }
}

TxtOverlay.prototype.toggle = function(){
    if (this.div_) {
        if (this.div_.style.visibility == "hidden") {
            this.show();
        }
        else {
            this.hide();
        }
    }
}

TxtOverlay.prototype.toggleDOM = function(){
    if (this.getMap()) {
        this.setMap(null);
    }
    else {
        this.setMap(this.map_);
    }
}

// Custom one I added
TxtOverlay.prototype.setTxt = function(text) {
//    this.txt_ = text
//    this.div_.innerHTML = this.txt_
    try {
        this.div_.innerHTML = text
    }
    catch(TypeError) {} // This will occur on the initial load only.
}