/* Chainage Management — JavaScript */
document.addEventListener("DOMContentLoaded", function () {
    // ── Map setup ──
    const map = L.map('chainageMap').setView([20.5937, 78.9629], 6);
    L.tileLayer('http://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
        attribution: '© Geobot'
    }).addTo(map);

    let routeLayer = null;
    let markerLayer = L.layerGroup().addTo(map);
    let eventLayer = L.layerGroup().addTo(map);
    let currentProjectId = null;

    // ── Project selector ──
    document.getElementById('chainageProject').addEventListener('change', function () {
        currentProjectId = this.value;
        if (!currentProjectId) return;
        loadRoute(currentProjectId);
        loadEvents(currentProjectId);
    });

    // ── Load and display route ──
    function loadRoute(projectId) {
        fetch(`/api/twopprojects/${projectId}/?format=json`)
            .then(r => r.json())
            .then(data => {
                if (routeLayer) map.removeLayer(routeLayer);
                markerLayer.clearLayers();

                if (data.geometry && data.geometry.type) {
                    routeLayer = L.geoJSON(data.geometry, {
                        style: { color: '#0d6efd', weight: 5, opacity: 0.8 }
                    }).addTo(map);
                    map.fitBounds(routeLayer.getBounds(), { padding: [30, 30] });
                }

                // Route info panel
                const props = data.properties || {};
                const info = document.getElementById('routeInfoPanel');
                const roadType = props.road_type_detail
                    ? `${props.road_type_detail.name} (${props.road_type_detail.code})`
                    : '-';
                info.innerHTML = `
                    <p><strong>Name:</strong> ${props.twopname || '-'}</p>
                    <p><strong>Road Type:</strong> ${roadType}</p>
                    <p><strong>Status:</strong> ${props.twopstatus || '-'}</p>
                    <p><strong>Lanes:</strong> ${props.lanes || '-'}</p>
                    <p><strong>Width:</strong> ${props.carriageway_width ? props.carriageway_width + ' m' : '-'}</p>
                    <p><strong>Start Ch:</strong> ${props.start_chainage || 0} m</p>
                    <p><strong>End Ch:</strong> ${props.end_chainage ? props.end_chainage.toFixed(0) + ' m' : '-'}</p>
                `;
            })
            .catch(err => console.error('Error loading route:', err));
    }

    // ── Click on map to get chainage ──
    map.on('click', function (e) {
        document.getElementById('eventLat').value = e.latlng.lat.toFixed(6);
        document.getElementById('eventLng').value = e.latlng.lng.toFixed(6);

        if (currentProjectId) {
            const csrfInput = document.querySelector('#addEventForm [name=csrfmiddlewaretoken]');
            fetch(`/api/chainage-from-point/${currentProjectId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfInput ? csrfInput.value : '',
                },
                body: JSON.stringify({
                    lat: e.latlng.lat,
                    lng: e.latlng.lng,
                }),
            })
                .then(r => r.json())
                .then(data => {
                    if (data.chainage !== undefined) {
                        document.getElementById('eventChainage').value = data.chainage;
                        document.getElementById('chainageInfo').textContent =
                            `Clicked chainage: ${data.chainage} m (${(data.chainage / 1000).toFixed(2)} km)`;
                    }
                })
                .catch(err => console.error('Error computing chainage:', err));
        }
    });

    // ── Show chainage markers ──
    document.getElementById('btnShowMarkers').addEventListener('click', function () {
        if (!currentProjectId) {
            alert('Please select a project first.');
            return;
        }
        const interval = document.getElementById('markerInterval').value || 1000;
        markerLayer.clearLayers();

        fetch(`/api/chainage-markers/${currentProjectId}/?interval=${interval}`)
            .then(r => r.json())
            .then(data => {
                if (data.markers) {
                    data.markers.forEach(m => {
                        const icon = L.divIcon({
                            className: 'chainage-label',
                            html: `<span>${m.label}</span>`,
                            iconSize: [60, 20],
                            iconAnchor: [30, 10],
                        });
                        L.marker([m.lat, m.lng], { icon: icon })
                            .bindPopup(`Chainage: ${m.chainage} m`)
                            .addTo(markerLayer);
                    });
                }
            })
            .catch(err => console.error('Error generating markers:', err));
    });

    // ── Clear markers ──
    document.getElementById('btnClearMarkers').addEventListener('click', function () {
        markerLayer.clearLayers();
        document.getElementById('chainageInfo').textContent = '';
    });

    // ── Load events for project ──
    function loadEvents(projectId) {
        fetch(`/api/chainage-events/?format=json&project=${projectId}`)
            .then(r => r.json())
            .then(data => {
                renderEventList(data);
                renderEventsOnMap(data);
            })
            .catch(err => console.error('Error loading events:', err));
    }

    function renderEventsOnMap(geojson) {
        eventLayer.clearLayers();
        if (!geojson.features) return;
        geojson.features.forEach(feature => {
            const props = feature.properties;
            const coords = feature.geometry.coordinates;
            const marker = L.marker([coords[1], coords[0]])
                .bindPopup(`
                    <strong>${props.event_type_display || props.event_type}</strong><br>
                    Chainage: ${props.chainage} m<br>
                    ${props.description || ''}
                `);
            eventLayer.addLayer(marker);
        });
    }

    function renderEventList(geojson) {
        const container = document.getElementById('eventListContainer');
        if (!geojson.features || geojson.features.length === 0) {
            container.innerHTML = '<p class="text-muted">No chainage events found.</p>';
            return;
        }
        let html = '<div class="list-group">';
        geojson.features.forEach(feature => {
            const p = feature.properties;
            html += `
                <div class="list-group-item">
                    <strong>${p.event_type_display || p.event_type}</strong>
                    <small class="text-muted d-block">Chainage: ${p.chainage} m</small>
                    <small class="text-muted">${p.description || ''}</small>
                </div>`;
        });
        html += '</div>';
        container.innerHTML = html;
    }

    // ── Add Event Form ──
    document.getElementById('addEventForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const form = e.target;
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

        const body = {
            project: form.querySelector('[name=project]').value,
            event_type: form.querySelector('[name=event_type]').value,
            chainage: parseFloat(form.querySelector('[name=chainage]').value),
            location: {
                type: 'Point',
                coordinates: [
                    parseFloat(form.querySelector('[name=lng]').value),
                    parseFloat(form.querySelector('[name=lat]').value),
                ]
            },
            description: form.querySelector('[name=description]').value,
        };

        fetch('/api/chainage-events/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(body),
        })
            .then(r => {
                if (r.ok) {
                    alert('Chainage event added!');
                    form.reset();
                    if (currentProjectId) loadEvents(currentProjectId);
                } else {
                    r.json().then(d => alert('Error: ' + JSON.stringify(d)));
                }
            })
            .catch(err => alert('Network error: ' + err));
    });
});
