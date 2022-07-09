const initialLat = -34.9187;
const initialLng = -57.956;
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';


export function Map({selector, addSearch}){
    let marker;
    let map;
    let drawItems = new L.featureGroup();


// Instanciacion del mapa
initializeMap(selector);

if (addSearch){
    addSearchControl();
};

map.addEventListener('click', (e) => {addMarker(e.latlng)});

// Creacion del mapa
function initializeMap(selector){  
    map = L.map(selector).setView([initialLat, initialLng], 12);
    L.tileLayer(mapLayerUrl).addTo(map);

    map.addLayer(drawItems);
};

};

