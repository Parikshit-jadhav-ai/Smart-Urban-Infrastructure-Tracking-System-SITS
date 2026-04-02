import os
from django.contrib.gis.utils import LayerMapping
from .models import countryboundery, districtsboundery

# Auto-generated `LayerMapping` dictionary for countryboundery model
countryboundery_mapping = {
    'name': 'Name',
    'type': 'Type',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for districtsboundery model
districtsboundery_mapping = {
    'dist_name': 'Dist_Name',
    'state_name': 'State_Name',
    'geom': 'MULTIPOLYGON',
}
countryshp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/SID/Envs/geoapp/geobot/geodata/India_State_Shapefile/India_State_Boundary.shp'))

def run(verbose= True):
    lm = LayerMapping(countryboundery, countryshp, countryboundery_mapping, transform=False, encoding="iso-8859-1")
    lm.save(strict=True,verbose= verbose)

districtshp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/SID/Envs/geoapp/geobot/geodata/India_District_Shapefile/India_Districts.shp'))

def drun(verbose= True):
    lm = LayerMapping(districtsboundery, districtshp, districtsboundery_mapping, transform=False, encoding="iso-8859-1")
    lm.save(strict=True,verbose= verbose)
