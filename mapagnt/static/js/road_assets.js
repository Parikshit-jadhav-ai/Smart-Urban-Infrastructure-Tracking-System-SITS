/* Road Asset Management — JavaScript */
document.addEventListener("DOMContentLoaded", function () {
    // ── Map setup ──
    const map = L.map('assetMap').setView([20.5937, 78.9629], 6);
    L.tileLayer('http://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
        attribution: '© Geobot'
    }).addTo(map);

    let assetMarkers = L.layerGroup().addTo(map);

    // Condition color mapping
    const conditionColors = {
        good: '#28a745',
        moderate: '#ffc107',
        poor: '#fd7e14',
        critical: '#dc3545',
    };

    // ── Click map to fill lat/lng ──
    map.on('click', function (e) {
        document.getElementById('assetLat').value = e.latlng.lat.toFixed(6);
        document.getElementById('assetLng').value = e.latlng.lng.toFixed(6);
    });

    // ── Fetch and render assets ──
    function loadAssets() {
        const projectId = document.getElementById('filterProject').value;
        const assetType = document.getElementById('filterAssetType').value;
        const condition = document.getElementById('filterCondition').value;

        let url = '/api/road-assets/?format=json';
        if (projectId) url += `&project=${projectId}`;
        if (assetType) url += `&asset_type=${assetType}`;
        if (condition) url += `&condition=${condition}`;

        fetch(url)
            .then(r => r.json())
            .then(data => {
                renderAssetsOnMap(data);
                renderAssetList(data);
                renderConditionSummary(data);
            })
            .catch(err => console.error('Error loading assets:', err));
    }

    function renderAssetsOnMap(geojson) {
        assetMarkers.clearLayers();
        if (!geojson.features) return;

        geojson.features.forEach(feature => {
            const props = feature.properties;
            const coords = feature.geometry.coordinates;
            const color = conditionColors[props.condition] || '#6c757d';

            const marker = L.circleMarker([coords[1], coords[0]], {
                radius: 8,
                fillColor: color,
                color: '#fff',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.85,
            });

            marker.bindPopup(`
                <strong>${props.asset_type_display || props.asset_type}</strong><br>
                Condition: <span style="color:${color};font-weight:bold">${props.condition_display || props.condition}</span><br>
                Chainage: ${props.chainage}m<br>
                Project: ${props.project_name || '-'}
            `);

            assetMarkers.addLayer(marker);
        });
    }

    function renderAssetList(geojson) {
        const container = document.getElementById('assetListContainer');
        if (!geojson.features || geojson.features.length === 0) {
            container.innerHTML = '<p class="text-muted">No assets found.</p>';
            return;
        }

        let html = '<div class="list-group">';
        geojson.features.forEach(feature => {
            const p = feature.properties;
            const color = conditionColors[p.condition] || '#6c757d';
            html += `
                <div class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${p.asset_type_display || p.asset_type}</strong>
                        <small class="text-muted d-block">Ch: ${p.chainage}m | ${p.project_name || '-'}</small>
                    </div>
                    <span class="badge" style="background:${color};color:#fff">${p.condition_display || p.condition}</span>
                </div>`;
        });
        html += '</div>';
        container.innerHTML = html;
    }

    function renderConditionSummary(geojson) {
        const container = document.getElementById('conditionSummary');
        if (!geojson.features) {
            container.innerHTML = '';
            return;
        }
        const counts = { good: 0, moderate: 0, poor: 0, critical: 0 };
        geojson.features.forEach(f => {
            const c = f.properties.condition;
            if (counts[c] !== undefined) counts[c]++;
        });

        let html = '';
        for (const [key, val] of Object.entries(counts)) {
            const color = conditionColors[key];
            html += `<span class="badge p-2" style="background:${color};color:#fff;font-size:0.85rem">${key}: ${val}</span>`;
        }
        html += `<span class="badge p-2 bg-secondary" style="font-size:0.85rem">Total: ${geojson.features.length}</span>`;
        container.innerHTML = html;
    }

    // ── Filter button ──
    document.getElementById('btnApplyFilter').addEventListener('click', loadAssets);

    // ── Add Asset Form ──
    document.getElementById('addAssetForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const form = e.target;
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

        const body = {
            project: form.querySelector('[name=project]').value,
            asset_type: form.querySelector('[name=asset_type]').value,
            condition: form.querySelector('[name=condition]').value,
            chainage: parseFloat(form.querySelector('[name=chainage]').value),
            location: {
                type: 'Point',
                coordinates: [
                    parseFloat(form.querySelector('[name=lng]').value),
                    parseFloat(form.querySelector('[name=lat]').value),
                ]
            },
            installation_date: form.querySelector('[name=installation_date]').value || null,
        };

        fetch('/api/road-assets/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(body),
        })
            .then(r => {
                if (r.ok) {
                    alert('Asset added successfully!');
                    form.reset();
                    loadAssets();
                } else {
                    r.json().then(d => alert('Error: ' + JSON.stringify(d)));
                }
            })
            .catch(err => alert('Network error: ' + err));
    });

    // Initial load
    loadAssets();
});
