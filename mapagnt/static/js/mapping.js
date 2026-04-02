document.addEventListener("DOMContentLoaded", function() {
    const map = L.map('mapone').setView([51.505, -0.09], 13);

    L.tileLayer('http://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Function to add markers to the map
    function addMarkersToMap(oneprojects) {
        oneprojects.forEach(function(oneproject) {
            const { onepname, oneplatitude, oneplongitude } = oneproject;
            
            if (oneplatitude && oneplongitude) {
                const marker = L.marker([parseFloat(oneplatitude), parseFloat(oneplongitude)])
                    .bindPopup(`<b>${onepname}</b>`)
                    .addTo(map);
            }
        });
    }

    // Fetch data from Django backend and add markers
    fetch('{% url "fetch_oneprojects" %}')
        .then(response => response.json())
        .then(data => {
            addMarkersToMap(data.oneprojects);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});