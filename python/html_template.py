#!/usr/bin/env python
#HTML template for Mode S map display
#Nick Foster, 2013

def html_template(my_position, json_file):
    if my_position is None:
        my_position = [37, -122]
        
    return """
<html>
    <head>
        <title>ADS-B Aircraft Map</title>
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
        <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false">
        </script>
        <script type="text/javascript">
            var map;
            var markers = [];
            var defaultLocation = new google.maps.LatLng(%f, %f);
            var defaultZoomLevel = 9;

            function requestJSONP() {
                var script = document.createElement("script");
                script.src = "%s?" + Math.random();
                script.params = Math.random();
                document.getElementsByTagName('head')[0].appendChild(script);
            };

            var planeMarker;
            var planes = [];

            function clearMarkers() {
                for (var i = 0; i < planes.length; i++) {
                    planes[i].setMap(null);
                }
                planes = [];
            };

            function jsonp_callback(results) { // from JSONP
                clearMarkers();
                airplanes = {};
                for (var i = 0; i < results.length; i++) {
                    airplanes[results[i].icao] = {
                        center: new google.maps.LatLng(results[i].lat, results[i].lon),
                        heading: results[i].hdg,
                        altitude: 0
                    };
                }
                refreshIcons();
            }
            
            function refreshIcons() {
                for (var airplane in airplanes) {
                    var plane_icon = {
                        url: "http://www.nerdnetworks.org/~bistromath/airplane_sprite.png",
                        size: new google.maps.Size(128,128),
                        origin: new google.maps.Point(parseInt(airplanes[airplane].heading/10)*128,0),
                        anchor: new google.maps.Point(64,64),
                        //scaledSize: new google.maps.Size(4608,126)
                    };
                    var planeOptions = {
                        map: map,
                        position: airplanes[airplane].center,
                        icon: plane_icon
                    };
                    planeMarker = new google.maps.Marker(planeOptions);
                    planes.push(planeMarker);
                };
            };

            function initialize()
            {
            	var myOptions = 
            	{
            		zoom: defaultZoomLevel,
            		center: defaultLocation,
            		disableDefaultUI: true,
            		mapTypeId: google.maps.MapTypeId.TERRAIN
            	};

                map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

                requestJSONP();
                setInterval("requestJSONP()", 1000);
            };
        </script>
    </head>
    <body onload="initialize()">
        <div id="map_canvas" style="width:100%%; height:100%%">
        </div>
    </body>
</html>""" % (my_position[0], my_position[1], json_file)
