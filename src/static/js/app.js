function initMap(){
    var littleton = L.marker([39.61, -105.02]).bindPopup('This is Littleton, CO.'),
    denver    = L.marker([39.74, -104.99]).bindPopup('This is Denver, CO.'),
    aurora    = L.marker([39.73, -104.8]).bindPopup('This is Aurora, CO.'),
    golden    = L.marker([39.77, -105.23]).bindPopup('This is Golden, CO.');

    var cities = L.layerGroup([littleton, denver, aurora, golden]);
    var streets = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.mapbox-terrain-v2',
        accessToken: 'pk.eyJ1IjoibmVtb25lc3N1bm8iLCJhIjoiY2phM3FvbGRkM2x6MTM0cGN1M3h6dHcyYiJ9.Gie5hDNbis60D17BFvH31Q'
    });

    var drawnItems = new L.FeatureGroup();
    var drawControl = new L.Control.Draw({
        draw: false,
        edit: {
            featureGroup: drawnItems,
            remove: false,
            edit: {
                selectedPathOptions: {
                    color: '#FF5500',
                    opacity: 1,
                    weight: 2
                }
            }
        }
    });
    drawnItems.addLayer(L.polygon([
        [39.11, -105.02],
        [38.71, -104.1],
        [38.71, -103.1],
        [40.21, -105.98]
    ]));
    drawnItems.addLayer(L.polygon([
        [36.21, -105.98],
        [37.11, -105.02],
        [38.71, -104.1],
        [38.71, -103.1]
    ]));


    var overlayMaps = {
        "Cities": cities,
        "Editable": drawnItems
    };

     var map = L.map('mapid', {
        center:[39.61, -105.02],
        zoom: 8,
        maxzoom: 13,
        layers: [drawnItems, cities, streets]
        });
     map.addControl(drawControl)

    L.control.layers({}, overlayMaps, drawnItems).addTo(map);
}

function initPolygon(coordinates){

}