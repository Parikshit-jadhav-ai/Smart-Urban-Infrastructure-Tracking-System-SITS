import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point, LineString
from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.db.models import Count, Sum, Q

from .models import (
    onepproject, twopproject, projectcoordinator,
    countryboundery, districtsboundery,
    RoadType, ChainageEvent, RoadAsset, AssetInspection,
)
from .serializers import (
    ProjectCoordinatorSerializer, OneProjectSerializer,
    TwoProjectSerializer, CountryBoundarySerializer,
    DistrictBoundarySerializer, RoadTypeSerializer,
    ChainageEventSerializer, RoadAssetSerializer,
    AssetInspectionSerializer,
)


# ═══════════════════════════════════════════════════════════════════════════════
#  Page Views
# ═══════════════════════════════════════════════════════════════════════════════

def homepage(request):
    return render(request, 'home.html')


def dashboard(request):
    oneproject_types = onepproject.ONEPROJECT_TYPES
    oneproject_statuses = onepproject.ONEPROJECT_STATUS_CHOICES
    twoproject_types = twopproject.TWOPROJECT_TYPES
    twoproject_statuses = twopproject.TWOPROJECT_STATUS_CHOICES

    # Road statistics
    total_onep = onepproject.objects.count()
    total_twop = twopproject.objects.count()
    total_projects = total_onep + total_twop

    completed_onep = onepproject.objects.filter(onepstatus='Completed').count()
    completed_twop = twopproject.objects.filter(twopstatus='Completed').count()
    completed_projects = completed_onep + completed_twop

    in_progress = total_projects - completed_projects

    # Asset statistics
    total_assets = RoadAsset.objects.count()
    assets_good = RoadAsset.objects.filter(condition='good').count()
    assets_moderate = RoadAsset.objects.filter(condition='moderate').count()
    assets_poor = RoadAsset.objects.filter(condition='poor').count()
    assets_critical = RoadAsset.objects.filter(condition='critical').count()

    # Road type counts
    road_type_counts = list(
        twopproject.objects.filter(road_type__isnull=False)
        .values('road_type__code', 'road_type__name')
        .annotate(count=Count('id'))
    )

    return render(request, 'dashboard.html', {
        'oneproject_types': oneproject_types,
        'oneproject_statuses': oneproject_statuses,
        'twoproject_types': twoproject_types,
        'twoproject_statuses': twoproject_statuses,
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'in_progress': in_progress,
        'total_assets': total_assets,
        'assets_good': assets_good,
        'assets_moderate': assets_moderate,
        'assets_poor': assets_poor,
        'assets_critical': assets_critical,
        'road_type_counts': road_type_counts,
    })


def operations(request):
    oneproject_types = onepproject.ONEPROJECT_TYPES
    oneproject_statuses = onepproject.ONEPROJECT_STATUS_CHOICES
    twoproject_types = twopproject.TWOPROJECT_TYPES
    twoproject_statuses = twopproject.TWOPROJECT_STATUS_CHOICES
    return render(request, 'operations.html', {
        'oneproject_types': oneproject_types,
        'oneproject_statuses': oneproject_statuses,
        'twoproject_types': twoproject_types,
        'twoproject_statuses': twoproject_statuses,
    })


def operationsse(request):
    oneproject_types = onepproject.ONEPROJECT_TYPES
    oneproject_statuses = onepproject.ONEPROJECT_STATUS_CHOICES
    twoproject_types = twopproject.TWOPROJECT_TYPES
    twoproject_statuses = twopproject.TWOPROJECT_STATUS_CHOICES
    road_types = RoadType.objects.all()
    return render(request, 'operationsse.html', {
        'oneproject_types': oneproject_types,
        'oneproject_statuses': oneproject_statuses,
        'twoproject_types': twoproject_types,
        'twoproject_statuses': twoproject_statuses,
        'road_types': road_types,
    })


def route(request):
    return render(request, 'routing.html')


def maproute(request):
    twopprojects = list(twopproject.objects.all().values(
        'twopname', 'twopstartlat', 'twopstartlon',
        'twopendlat', 'twopendlon'))
    context = {'twopprojects': twopprojects}
    return render(request, 'map.html', context)


def road_assets_page(request):
    """Render the Road Asset Management page."""
    projects = twopproject.objects.all()
    asset_types = RoadAsset.ASSET_TYPES
    condition_choices = RoadAsset.CONDITION_CHOICES
    return render(request, 'road_assets.html', {
        'projects': projects,
        'asset_types': asset_types,
        'condition_choices': condition_choices,
    })


def chainage_page(request):
    """Render the Chainage Management page."""
    projects = twopproject.objects.filter(route__isnull=False)
    event_types = ChainageEvent.EVENT_TYPES
    return render(request, 'chainage.html', {
        'projects': projects,
        'event_types': event_types,
    })


# ═══════════════════════════════════════════════════════════════════════════════
#  Data fetch views
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_allprojects(request):
    onepprojects = list(onepproject.objects.all().values(
        'onepname', 'oneplatitude', 'oneplongitude'))
    twopprojects = list(twopproject.objects.all().values(
        'twopname', 'twopstartlat', 'twopstartlon',
        'twopendlat', 'twopendlon'))
    all_projects = onepprojects + twopprojects
    return JsonResponse({'allprojects': all_projects})


# ═══════════════════════════════════════════════════════════════════════════════
#  Project CRUD (form-based)
# ═══════════════════════════════════════════════════════════════════════════════

def create_onepproject(request):
    if request.method == 'POST':
        onepname = request.POST.get('onepname')
        oneptype = request.POST.get('oneptype')
        onepbudget = request.POST.get('onepbudget')
        onepstatus = request.POST.get('onepstatus')
        coordinatorname = request.POST.get('coordinatorname')
        onepdescription = request.POST.get('onepdescription')
        onepaddress = request.POST.get('onepaddress')
        oneplatitude = request.POST.get('oneplatitude')
        oneplongitude = request.POST.get('oneplongitude')

        new_onepproject = onepproject.objects.create(
            onepname=onepname,
            oneptype=oneptype,
            onepbudget=onepbudget,
            onepstatus=onepstatus,
            onecoordinatorname=coordinatorname,
            onepdescription=onepdescription,
            onepaddress=onepaddress,
            oneplatitude=oneplatitude,
            oneplongitude=oneplongitude,
            oneplocation=create_point_from_lat_long(oneplatitude, oneplongitude),
        )
        new_onepproject.save()
        return redirect('successpage')
    else:
        project_types = onepproject.objects.values_list(
            'oneptype', flat=True).distinct()
        project_statuses = onepproject.objects.values_list(
            'onepstatus', flat=True).distinct()
        context = {
            'project_types': project_types,
            'project_statuses': project_statuses,
        }
    return render(request, 'operations.html', context)


def create_twopproject(request):
    if request.method == 'POST':
        twopname = request.POST.get('twopname')
        twoptype = request.POST.get('twoptype')
        twopbudget = request.POST.get('twopbudget')
        twopstatus = request.POST.get('twopstatus')
        twocoordinatorname = request.POST.get('twocoordinatorname')
        twopdescription = request.POST.get('twoonepdescription')
        twopaddress = request.POST.get('twopaddress')
        twopstartlat = request.POST.get('latitude1')
        twopstartlon = request.POST.get('longitude1')
        twopendlat = request.POST.get('latitude2')
        twopendlon = request.POST.get('longitude2')

        # New fields
        road_type_id = request.POST.get('road_type')
        carriageway_width = request.POST.get('carriageway_width') or None
        lanes = request.POST.get('lanes') or 2
        route_coords_json = request.POST.get('route_coords')

        # Build route LineString from coordinates if provided
        route_geom = None
        if route_coords_json:
            try:
                coords = json.loads(route_coords_json)
                if len(coords) >= 2:
                    route_geom = LineString(
                        [(c[1], c[0]) for c in coords], srid=4326)
            except (json.JSONDecodeError, TypeError):
                pass

        # If no drawn route, create line from start/end points
        if route_geom is None and twopstartlat and twopstartlon \
                and twopendlat and twopendlon:
            route_geom = LineString(
                (float(twopstartlon), float(twopstartlat)),
                (float(twopendlon), float(twopendlat)),
                srid=4326,
            )

        road_type = None
        if road_type_id:
            try:
                road_type = RoadType.objects.get(id=road_type_id)
            except RoadType.DoesNotExist:
                pass

        new_twopproject = twopproject.objects.create(
            twopname=twopname,
            twoptype=twoptype,
            twopbudget=twopbudget,
            twopstatus=twopstatus,
            twocoordinatorname=twocoordinatorname,
            twopdescription=twopdescription,
            twopaddress=twopaddress,
            twopstartlat=twopstartlat,
            twopstartlon=twopstartlon,
            twopstart_point=create_point_from_lat_long(
                twopstartlat, twopstartlon),
            twopendlat=twopendlat,
            twopendlon=twopendlon,
            twopend_point=create_point_from_lat_long(
                twopendlat, twopendlon),
            route=route_geom,
            start_chainage=0,
            end_chainage=(route_geom.length * 111320 if route_geom else None),
            road_type=road_type,
            carriageway_width=carriageway_width,
            lanes=int(lanes),
        )
        new_twopproject.save()
        return redirect('successpage')

    # GET request — render form with context
    road_types = RoadType.objects.all()
    oneproject_types = onepproject.ONEPROJECT_TYPES
    oneproject_statuses = onepproject.ONEPROJECT_STATUS_CHOICES
    twoproject_types = twopproject.TWOPROJECT_TYPES
    twoproject_statuses = twopproject.TWOPROJECT_STATUS_CHOICES
    return render(request, 'operationsse.html', {
        'oneproject_types': oneproject_types,
        'oneproject_statuses': oneproject_statuses,
        'twoproject_types': twoproject_types,
        'twoproject_statuses': twoproject_statuses,
        'road_types': road_types,
    })


def create_point_from_lat_long(latitude, longitude):
    """Create a Point object from latitude and longitude."""
    latitude = float(latitude)
    longitude = float(longitude)
    return Point(longitude, latitude)


def successpage(request):
    return render(request, 'projectsavesuccess.html')


def updatesuccesspage(request):
    return render(request, 'projectupdatesuccess.html')


# ═══════════════════════════════════════════════════════════════════════════════
#  GeoJSON boundary views
# ═══════════════════════════════════════════════════════════════════════════════

class mapindex(TemplateView):
    template_name = 'map.html'


def countrybounderydata(request):
    countrymodel = serialize('geojson', countryboundery.objects.all())
    return HttpResponse(countrymodel, content_type="json")


def districtsbounderydata(request):
    districtsmodel = serialize('geojson', districtsboundery.objects.all())
    return HttpResponse(districtsmodel, content_type="json")


# ═══════════════════════════════════════════════════════════════════════════════
#  Chainage Utility Endpoints
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['POST'])
def get_chainage_from_point(request, project_id):
    """Given a lat/lng, find the chainage along the project's route."""
    try:
        project = twopproject.objects.get(id=project_id)
    except twopproject.DoesNotExist:
        return Response({'error': 'Project not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if not project.route:
        return Response({'error': 'Project has no route geometry'},
                        status=status.HTTP_400_BAD_REQUEST)

    lat = float(request.data.get('lat'))
    lng = float(request.data.get('lng'))
    point = Point(lng, lat, srid=4326)

    # ST_LineLocatePoint returns fraction (0 to 1)
    fraction = project.route.project(point, normalized=True)
    total_length = project.route.length * 111320  # approximate meters
    chainage = fraction * total_length

    return Response({
        'chainage': round(chainage, 2),
        'fraction': round(fraction, 6),
        'total_length_m': round(total_length, 2),
    })


@api_view(['POST'])
def get_point_from_chainage(request, project_id):
    """Given a chainage value, find the lat/lng on the route."""
    try:
        project = twopproject.objects.get(id=project_id)
    except twopproject.DoesNotExist:
        return Response({'error': 'Project not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if not project.route:
        return Response({'error': 'Project has no route geometry'},
                        status=status.HTTP_400_BAD_REQUEST)

    chainage = float(request.data.get('chainage', 0))
    total_length = project.route.length * 111320
    fraction = chainage / total_length if total_length > 0 else 0
    fraction = max(0, min(1, fraction))

    point = project.route.interpolate(fraction, normalized=True)

    return Response({
        'lat': round(point.y, 6),
        'lng': round(point.x, 6),
        'chainage': round(chainage, 2),
    })


@api_view(['GET'])
def generate_chainage_markers(request, project_id):
    """Generate chainage markers every N meters along a route."""
    try:
        project = twopproject.objects.get(id=project_id)
    except twopproject.DoesNotExist:
        return Response({'error': 'Project not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if not project.route:
        return Response({'error': 'Project has no route geometry'},
                        status=status.HTTP_400_BAD_REQUEST)

    interval = float(request.query_params.get('interval', 1000))
    total_length = project.route.length * 111320
    markers = []
    chainage = 0

    while chainage <= total_length:
        fraction = chainage / total_length if total_length > 0 else 0
        fraction = min(fraction, 1.0)
        point = project.route.interpolate(fraction, normalized=True)
        markers.append({
            'chainage': round(chainage, 2),
            'label': f"{int(chainage / 1000)}+{int(chainage % 1000):03d}",
            'lat': round(point.y, 6),
            'lng': round(point.x, 6),
        })
        chainage += interval

    return Response({'markers': markers, 'total_length_m': round(total_length, 2)})


# ═══════════════════════════════════════════════════════════════════════════════
#  DRF ViewSets
# ═══════════════════════════════════════════════════════════════════════════════

class ProjectCoordinatorViewSet(viewsets.ModelViewSet):
    queryset = projectcoordinator.objects.all()
    serializer_class = ProjectCoordinatorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OneProjectViewSet(viewsets.ModelViewSet):
    queryset = onepproject.objects.all()
    serializer_class = OneProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TwoProjectViewSet(viewsets.ModelViewSet):
    queryset = twopproject.objects.all()
    serializer_class = TwoProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoadTypeViewSet(viewsets.ModelViewSet):
    queryset = RoadType.objects.all()
    serializer_class = RoadTypeSerializer


class ChainageEventViewSet(viewsets.ModelViewSet):
    queryset = ChainageEvent.objects.all()
    serializer_class = ChainageEventSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        project_id = self.request.query_params.get('project')
        event_type = self.request.query_params.get('event_type')
        if project_id:
            qs = qs.filter(project_id=project_id)
        if event_type:
            qs = qs.filter(event_type=event_type)
        return qs


class RoadAssetViewSet(viewsets.ModelViewSet):
    queryset = RoadAsset.objects.all()
    serializer_class = RoadAssetSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        project_id = self.request.query_params.get('project')
        asset_type = self.request.query_params.get('asset_type')
        condition = self.request.query_params.get('condition')
        if project_id:
            qs = qs.filter(project_id=project_id)
        if asset_type:
            qs = qs.filter(asset_type=asset_type)
        if condition:
            qs = qs.filter(condition=condition)
        return qs


class AssetInspectionViewSet(viewsets.ModelViewSet):
    queryset = AssetInspection.objects.all()
    serializer_class = AssetInspectionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        asset_id = self.request.query_params.get('asset')
        condition = self.request.query_params.get('condition')
        if asset_id:
            qs = qs.filter(asset_id=asset_id)
        if condition:
            qs = qs.filter(condition=condition)
        return qs
