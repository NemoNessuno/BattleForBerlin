var map;
var uwb;
var bwb;

var myStyle = {
    "color": "#ff7800",
    "weight": 1,
    "opacity": 0.65
};

function initMap(){
    var streets = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoibmVtb25lc3N1bm8iLCJhIjoiY2phM3FvbGRkM2x6MTM0cGN1M3h6dHcyYiJ9.Gie5hDNbis60D17BFvH31Q'
    });

    uwb = new L.FeatureGroup();
    bwb = new L.FeatureGroup();

    var overlayMaps = {
        "Urnenwahlbezirke": uwb,
        "Briefwahlbezirke": bwb
    };

     map = L.map('mapid', {
        center:[52.5200, 13.4050],
        zoom: 10,
        maxzoom: 13,
        layers: [uwb, bwb, streets]
        });

    L.control.layers({}, overlayMaps).addTo(map);
}

function initShape(geojsonFeature){
    L.geoJSON(geojsonFeature, {style: myStyle}).addTo(map);
}