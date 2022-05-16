var mymap = L.map('map').setView([59.62358439610628, 17.60429768165015], 13);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    attribution: '&copy; <a>AFirması GPS</a> Kocaeli, Universitesi © <a>Kinto Aden</a>',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1Ijoia2ludG8yNTE3IiwiYSI6ImNsMHFhZDc0cTI1Nnkza205Y2JicjQ3NHgifQ.o3ojgFylXi7j2lgBtsmi9g'
}).addTo(mymap);

mymap.zoomControl.setPosition('topleft');

L.control.scale({
    metric: true,
    imperial: false,
    position: 'bottomleft'
}).addTo(mymap);

L.Control.Watermark = L.Control.extend({
    onAdd: function (mymap) {
        var img = L.DomUtil.create('img');

        return img;
    },
    onRemove: function (mymap) {
    },
});

L.control.watermark = function (opts) {
    return new L.Control.Watermark(opts);
}
L.control.watermark({position: 'topright'}).addTo(mymap);


var mapId = document.getElementById('map');

function fullScreen() {
    mapId.requestFullscreen();
}


mapMarkers6 = [];
mapMarkers5 = [];


var markerM6 = L.icon({
    iconUrl: 'https://cdn-icons.flaticon.com/png/512/3710/premium/3710267.png?token=exp=1647334622~hmac=d4fe1887a6bf8dc25a8920b549b47e46',
    iconSize: [26, 27],
    iconAnchor: [22, 94],
    popupAnchor: [-3, -76],
});


var markerM7 = L.icon({
    iconUrl: 'https://cdn-icons.flaticon.com/png/512/3156/premium/3156200.png?token=exp=1647334672~hmac=93e29adec9e38fb6ad34be88f4825074',
    iconSize: [26, 27],
    iconAnchor: [22, 94],
    popupAnchor: [-3, -76],
});


const btn = document.querySelector('#submit');
const radioButtons = document.querySelectorAll('input[name="araclar"]');
const time1 = document.querySelector('#aracSaat');
const time2 = document.querySelector('#aracSaat2');

let selectedSize, fTime, lTime;
btn.addEventListener("click", function (event)  {
    for (const radioButton of radioButtons) {
        if (radioButton.checked) {
            selectedSize = radioButton.value;
            break;
        }
    }
    fTime = time1.value;
    lTime = time2.value;

    var source = new EventSource('/topic/bbbb');

    source.addEventListener('message', function (e) {
        console.log('Message');
        obj = JSON.parse(e.data);
        console.log(obj);
        console.log(selectedSize);
        console.log(fTime);
        console.log(lTime);

        if (selectedSize == "Arac 1") {
            if (obj.carid == carid1 && obj.timestamp <= lTime && obj.timestamp >= fTime) {
                console.log(obj.carid.toString())

                marker6 = L.marker([obj.latitude, obj.longtitude], {icon: markerM6}).addTo(mymap);
                marker6.bindPopup("Zaman: " + obj.timestamp + "\n" + "Arac ID: " + obj.carid).openPopup();
                mapMarkers6.push(marker6);

            }
        }

        if (selectedSize == "Arac 2") {
            if (obj.carid == carid2 && obj.timestamp <= lTime && obj.timestamp >= fTime) {
                console.log(obj.carid.toString())

                marker7 = L.marker([obj.latitude, obj.longtitude], {icon: markerM7}).addTo(mymap);
                marker7.bindPopup("Zaman: " + obj.timestamp + "\n" + "Arac ID: " + obj.carid).openPopup();
                mapMarkers7.push(marker7);

            }
        }

    }, false);
});


