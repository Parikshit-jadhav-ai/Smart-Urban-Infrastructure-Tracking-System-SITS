//<!-- Custom JavaScript -->
document.addEventListener("DOMContentLoaded", function() {
    const projects = [
        { id: 1, name: "Project 1", status: "completed", details: "Details for Project 1" },
        { id: 2, name: "Project 2", status: "inProgress", details: "Details for Project 2" },
        { id: 3, name: "Project 3", status: "completed", details: "Details for Project 3" },
        { id: 4, name: "Project 4", status: "inProgress", details: "Details for Project 4" },
        { id: 5, name: "Project 5", status: "completed", details: "Details for Project 5" },
        { id: 1, name: "Project 6", status: "completed", details: "Details for Project 1" },
        { id: 2, name: "Project 7", status: "inProgress", details: "Details for Project 2" },
        { id: 3, name: "Project 8", status: "completed", details: "Details for Project 3" },
        { id: 4, name: "Project 9", status: "inProgress", details: "Details for Project 4" },
        { id: 5, name: "Project 10", status: "completed", details: "Details for Project 5" },
    ];

    const projectListAllElement = document.getElementById("projectListAll");
    const projectListCompletedElement = document.getElementById("projectListCompleted");
    const projectListInProgressElement = document.getElementById("projectListInProgress");
    const searchInput = document.getElementById("searchInput");

    // Function to display projects based on search input
    function displayProjects(projects, targetElement) {
        targetElement.innerHTML = ""; // Clear previous list

        projects.forEach(project => {
            const listItem = document.createElement("li");
            listItem.className = "list-group-item d-flex justify-content-between align-items-center";
            listItem.innerHTML = `
                ${project.name}
                <div>
                    <button type="button" class="btn btn-edit btn-sm" onclick="editProject(${project.id})">Edit</button>
                    <button type="button" class="btn btn-delete btn-sm" onclick="deleteProject(${project.id})">Delete</button>
                    <button type="button" class="btn btn-showdetail btn-sm" onclick="showProjectDetails('${project.details}')">Show Details</button>
                </div>
            `;
            targetElement.appendChild(listItem);
        });
    }

    // Initial display of all projects
    displayProjects(projects, projectListAllElement);

    // Event listener for search input
    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.trim().toLowerCase();

        if (searchText === "") {
            displayProjects(projects, projectListAllElement); // Display all projects if search input is empty
        } else {
            const filteredProjects = projects.filter(project => project.name.toLowerCase().includes(searchText));
            displayProjects(filteredProjects, projectListAllElement); // Display filtered projects based on search text
        }
    });

    // Calculate project statistics
    const totalProjectsElement = document.getElementById("totalProjects");
    const completedProjectsElement = document.getElementById("completedProjects");
    const projectsInProgressElement = document.getElementById("projectsInProgress");

    const totalProjects = projects.length;
    const completedProjects = projects.filter(project => project.status === "completed").length;
    const projectsInProgress = totalProjects - completedProjects;

    totalProjectsElement.textContent = totalProjects;
    completedProjectsElement.textContent = completedProjects;
    projectsInProgressElement.textContent = projectsInProgress;
});


document.addEventListener("DOMContentLoaded", function() {
    const map = L.map('map').setView([20.5937, 78.9629], 13);

    L.tileLayer('http://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
        attribution: '© Matoshi collage of engg'
    }).addTo(map);

    // Initialize marker at a specific location
    const initialLatLng = [20.5937, 78.9629];
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

        const markerCoordinates = document.getElementById('markerCoordinates');
        markerCoordinates.innerHTML = `Latitude: ${lat}<br>Longitude: ${lng}`;
    }
});


// Function to handle editing a project (open modal, etc.)
function editProject(projectId) {
    console.log("Editing project with ID:", projectId);
}

// Function to handle deleting a project (confirm modal, API call, etc.)
function deleteProject(projectId) {
    console.log("Deleting project with ID:", projectId);
}

// Function to show project details
function showProjectDetails(details) {
    alert(details);
}