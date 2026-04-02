document.addEventListener("DOMContentLoaded", function() {
    const map = L.map('mapone').setView([19.9975, 73.7898], 13);

    L.tileLayer('http://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Initialize marker at a specific location19.9975° N, 73.7898
    const initialLatLng = [19.9975, 73.7898];
    const marker = L.marker(initialLatLng, { draggable: true }).addTo(map);

    // Display initial coordinates
    updateMarkerCoordinates(marker);

    // Event listener for marker drag
    marker.on('drag', function(event) {
        updateMarkerCoordinates(event.target);
    });
    function updateMarkerCoordinates(marker) {
        const lat = marker.getLatLng().lat.toFixed(6);
        const lng = marker.getLatLng().lng.toFixed(6);

        // Update latitude and longitude input fields
        document.getElementById('oneplatitude').value = lat;
        document.getElementById('oneplongitude').value = lng;

        // Display coordinates in a separate div
        const markerCoordinates = document.getElementById('markerCoordinatesone');
        markerCoordinates.innerHTML = `Latitude: ${lat}<br>Longitude: ${lng}`;
    }

            // Add click event listener to set marker position on map click
    map.on('click', function(e) {
        marker.setLatLng(e.latlng); // Set marker position
        updateMarkerCoordinates(marker); // Update input fields with new coordinates
    });
    
});
