# geobot Project Documentation

## 1. Overview
**geobot** is a GIS-powered project management system designed for infrastructure and civil engineering projects in India. It leverages GeoDjango and PostGIS to handle spatial data, allowing users to manage both fixed-location (Point) and route-based (Line/Route) projects on an interactive map.

## 2. Technical Stack
- **Backend Framework**: [Django](https://www.djangoproject.com/) (v5.0.2)
- **GIS Extension**: [GeoDjango](https://docs.djangoproject.com/en/5.0/ref/contrib/gis/)
- **API Framework**: [Django Rest Framework (DRF)](https://www.django-rest-framework.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) with [PostGIS](https://postgis.net/) extension
- **Frontend Mapping**: [Leaflet.js](https://leafletjs.com/)
- **Data Source**: India District and State Shapefiles

## 3. Project Architecture
The project is structured as a standard Django project with a core application named `mapagnt`.

- `geobot/`: Project configuration, settings, and root URL routing.
- `mapagnt/`: Main application logic, including models, views, and static assets.
- `geodata/`: Storage for geographic shapefiles.

## 4. Core Data Models

### 4.1 Project Coordinator (`projectcoordinator`)
Stores information about the individuals managing the projects.
- Fields: `coordinatorname`, `coordinatordesignation`, `coordinatoremail`, `coordinatorphnumber`, etc.

### 4.2 One-Point Project (`onepproject`)
Represents fixed-location projects such as municipal facilities, parks, or police stations.
- Geographic Field: `oneplocation` (PointField)
- Attributes: `onepname`, `oneptype`, `onepbudget`, `onepstatus`, `onepdescription`.

### 4.3 Two-Point Project (`twopproject`)
Represents linear projects such as pipelines, highways, or road rehabilitation.
- Geographic Fields: `twopstart_point` (PointField), `twopend_point` (PointField)
- Attributes: `twopname`, `twoptype`, `twopbudget`, `twopstatus`, `twopdescription`.

### 4.4 Boundary Models
Used to store and serve geographic boundaries for visualization.
- `countryboundery`: MultiPolygon representation of country borders.
- `districtsboundery`: MultiPolygon representation of district borders (includes `state_name`).

## 5. Geographic Data Handling
- **Shapefile Loading**: Geographic data is imported using the `ogrinspect` utility (as seen in `loaddata.txt`).
- **Data Service**: Boundaries are served as GeoJSON via dedicated views (`countrybounderydata`, `districtsbounderydata`).
- **Spatial Queries**: Managed using GeoDjango's `GeoManager`, allowing for spatial operations like distance calculations or intersection checks.

## 6. Frontend Interaction
- **Interactive Map**: Centered on India, utilizing Google Hybrid satellite imagery.
- **Project Visualization**: Projects are displayed as markers or lines on the map.
- **Dashboard**: A comprehensive interface for tracking project counts (Total, Completed, In-Progress) and searching through the project list.

## 7. API Reference
The project provides a RESTful API under `/api/`:
- `/api/projectcoordinators/`: CRUD for project coordinators.
- `/api/onepprojects/`: CRUD for one-point projects (GeoJSON compatible).
- `/api/twopprojects/`: CRUD for two-point projects (GeoJSON compatible).

## 8. Installation and Setup

### Prerequisites
- Python 3.10+
- PostgreSQL with PostGIS extension
- Virtual Environment (recommended)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd geobot
   ```
2. **Install Dependencies**:
   ```bash
   pip install django djangorestframework django-leaflet django-rest-framework-gis psycopg2-binary
   ```
3. **Database Configuration**:
   Create a PostgreSQL database named `geodatamldl` and enable the PostGIS extension:
   ```sql
   CREATE DATABASE geodatamldl;
   \c geodatamldl
   CREATE EXTENSION postgis;
   ```
4. **Update Settings**:
   Ensure `geobot/settings.py` has the correct database credentials.
5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
7. **Access the Application**:
   Open `http://127.0.0.1:8000/` in your browser.
