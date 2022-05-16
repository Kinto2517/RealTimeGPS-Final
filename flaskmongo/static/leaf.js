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
    onAdd:function (mymap){
        var img = L.DomUtil.create('img');
        img.src = 'https://cdn-icons.flaticon.com/png/512/3170/premium/3170183.png?token=exp=1647429254~hmac=e4270674971fe0eb2151cdd2119fb345'
        img.style.width = '40px';
        img.style.height = '40px'
        return img;
    },
    onRemove:function (mymap){},
});

L.control.watermark = function (opts){
    return new L.Control.Watermark(opts);
}
L.control.watermark({position: 'topright'}).addTo(mymap);



var mapId = document.getElementById('map');
function fullScreen(){
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


var source = new EventSource('/topic/bbbb');


source.addEventListener('message', function (e) {
    console.log('Message');
    obj = JSON.parse(e.data);
    console.log(obj);

    var minutesToAdd = 30;
    var currentDate = new Date();
    var pastDate = new Date(currentDate - minutesToAdd * 60000);

    if (pastDate.getMinutes().toString().length == 1) {
        if (pastDate.getHours() < 10) {
            dformat1 = ["0" + pastDate.getHours(), "0" + pastDate.getMinutes()].join(':');
            console.log(dformat1)
        } else {
            dformat1 = [pastDate.getHours(), "0" + pastDate.getMinutes()].join(':');
            console.log(dformat1)
        }
    } else {
        if (pastDate.getHours() < 10) {
            dformat1 = ["0" + pastDate.getHours(), pastDate.getMinutes()].join(':');
            console.log(dformat1)
        } else {
            dformat1 = [pastDate.getHours(), pastDate.getMinutes()].join(':');
            console.log(dformat1)
        }
    }

if (currentDate.getMinutes().toString().length == 1) {
        if (currentDate.getHours() < 10) {
            dformat = ["0" + currentDate.getHours(), "0" + currentDate.getMinutes()].join(':');
            console.log(dformat)
        } else {
            dformat = [currentDate.getHours(), "0" + currentDate.getMinutes()].join(':');
            console.log(dformat)
        }
    } else {
        if (currentDate.getHours() < 10) {
            dformat = ["0" + currentDate.getHours(), currentDate.getMinutes()].join(':');
            console.log(dformat)
        } else {
            dformat = [currentDate.getHours(), currentDate.getMinutes()].join(':');
            console.log(dformat)
        }
    }


    if (obj.carid == carid1 && obj.timestamp <= dformat && obj.timestamp > dformat1) {
        console.log(obj.carid.toString())

        marker3 = L.marker([obj.latitude, obj.longtitude], {icon: markerM3}).addTo(mymap);
        marker3.bindPopup("Zaman: " + obj.timestamp + "\n" + "Arac ID: " + obj.carid).openPopup();
        mapMarkers3.push(marker3);

    }

    if (obj.carid == carid2 && obj.timestamp <= dformat && obj.timestamp > dformat1) {
        console.log(obj.carid.toString())

        marker5 = L.marker([obj.latitude, obj.longtitude], {icon: markerM5}).addTo(mymap);
        marker5.bindPopup("Zaman: " + obj.timestamp + "\n" + "Arac ID: " + obj.carid).openPopup();
        mapMarkers5.push(marker5);

    }

}, false);
