document.addEventListener("DOMContentLoaded", function() {
    var map = L.map('maptwo').setView([19.9975, 73.7898], 13);

    L.tileLayer('http://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Array to store markers and their coordinates
    const markers = [];
    const routeCoords = [];
    let routeLine = null;

    // Event listener for map click to place markers and draw route
    map.on('click', function(e) {
        const lat = e.latlng.lat.toFixed(6);
        const lng = e.latlng.lng.toFixed(6);

        // Create marker and add to map
        const marker = L.marker(e.latlng).addTo(map);
        markers.push(marker);
        routeCoords.push([parseFloat(lat), parseFloat(lng)]);

        // Update input fields based on marker index
        const index = markers.length;
        if (index === 1) {
            document.getElementById('latitude1').value = lat;
            document.getElementById('longitude1').value = lng;
        } else if (index === 2) {
            document.getElementById('latitude2').value = lat;
            document.getElementById('longitude2').value = lng;
        }

        // Draw/update route line if we have 2+ points
        if (routeCoords.length >= 2) {
            if (routeLine) map.removeLayer(routeLine);
            routeLine = L.polyline(routeCoords, {
                color: '#0d6efd',
                weight: 4,
                opacity: 0.8,
            }).addTo(map);
        }

        // Store route coordinates as hidden field for form submission
        const routeInput = document.getElementById('route_coords');
        if (routeInput) {
            routeInput.value = JSON.stringify(routeCoords);
        }
    });
});