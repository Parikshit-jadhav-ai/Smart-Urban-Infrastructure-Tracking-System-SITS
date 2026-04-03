# geobot - GIS-Powered Infrastructure Management

**geobot** is a GIS-based project management platform for India. It allows for the efficient planning and tracking of infrastructure projects, including fixed-location facilities and linear route projects like pipelines and highways.

## Key Features
- **Interactive GIS Map**: Visualize projects on a satellite map of India.
- **Project Tracking**: Manage "One-Point" (fixed) and "Two-Point" (route) projects.
- **Boundary Layers**: High-resolution district and state boundaries for India.
- **Real-time Statistics**: Dashboard for monitoring project progress and budgets.
- **REST API**: Full API support for integration with other systems.

## Tech Stack
- **Backend**: Django 5, GeoDjango, DRF, PostGIS.
- **Frontend**: Leaflet.js, JavaScript, HTML5/CSS3.

## Quick Start
1. Ensure PostgreSQL and PostGIS are installed.
2. Create a database named `geodatamldl`.
3. Install requirements: `pip install django djangorestframework django-leaflet django-rest-framework-gis psycopg2-binary`.
4. Run migrations: `python manage.py migrate`.
5. Run server: `python manage.py runserver`.

For more details, see the [Full Project Documentation](PROJECT_DOCUMENTATION.md).
# Smart-Urban-Infrastructure-Tracking-System-SITS
