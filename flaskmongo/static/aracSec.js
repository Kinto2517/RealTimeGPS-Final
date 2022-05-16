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


mapMarkers3 = [];
mapMarkers5 = [];


var markerM3 = L.icon({
    iconUrl: 'https://cdn-icons.flaticon.com/png/512/1048/premium/1048361.png?token=exp=1647259102~hmac=73439bc31e0980bd391c1f297877476d',
    iconSize: [26, 27],
    iconAnchor: [22, 94],
    popupAnchor: [-3, -76],
});


var markerM5 = L.icon({
    iconUrl: 'https://cdn-icons.flaticon.com/png/512/1048/premium/1048315.png?token=exp=1647259164~hmac=d0c166deb71eb00f645ba421b36bb287',
    iconSize: [26, 27],
    iconAnchor: [22, 94],
    popupAnchor: [-3, -76],
});


const btn = document.querySelector('#submit');
const radioButtons = document.querySelectorAll('input[name="araclar"]');
const time1 = document.querySelector('#aracSaat');
const time2 = document.querySelector('#aracSaat2');


let selectedSize, fTime, lTime;
btn.addEventListener("click", function (event) {
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

                marker3 = L.marker([obj.latitude, obj.longtitude], {icon: markerM3}).addTo(mymap);
                marker3.bindPopup("Zaman: " + obj.timestamp + "\n" + "Arac ID: " + obj.carid).openPopup();
                mapMarkers3.push(marker3);

            }
        }

        if (selectedSize == "Arac 2") {
            if (obj.carid == carid2 && obj.timestamp <= lTime && obj.timestamp >= fTime) {
                console.log(obj.carid.toString())

                marker5 = L.marker([obj.latitude, obj.longtitude], {icon: markerM5}).addTo(mymap);
                marker5.bindPopup("Zaman: " + obj.timestamp + "\n" + "Arac ID: " + obj.carid).openPopup();
                mapMarkers5.push(marker5);

            }
        }

    }, false);
});


