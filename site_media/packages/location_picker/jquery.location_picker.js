google.load('maps', '2');

$(document).unload(function(){
    GUnload();
});

$(document).ready(function(){
    $('input.location_picker').each(function (i) {
        var map = document.createElement('div');
        map.className = 'location_picker_map';
        this.parentNode.insertBefore(map, this);
        $(this).css('display','none');

        var lat = 18.1758191780913;
        var lng = -66.15983033145312;
        var zoom = 13;
        if (this.value.split(',').length >= 2) {
            values = this.value.split(',');
            lat = values[0];
            lng = values[1];
            zoom = parseInt(values[2]);
        }
		if (!zoom) {
			zoom = 10;
		}
        var center = new GLatLng(lat,lng);
        var map = new google.maps.Map2(map);
        //map.addControl(new GSmallMapControl());
		map.addControl(new GLargeMapControl3D());
		map.addControl(new GMapTypeControl());
		map.setCenter(center, zoom);

        this.onMapClick = function(overlay, point) {
            this.value = point.lat()+','+point.lng()+','+map.getZoom();
            if (this.marker == null) {
                this.marker = new GMarker(point);
                this.map.addOverlay(this.marker);
            } else {
                this.marker.setPoint(point);
            }
        }

        this.marker = new GMarker(center);
        map.addOverlay(this.marker);

        GEvent.bind(map, 'click', this, this.onMapClick);
    });
});
