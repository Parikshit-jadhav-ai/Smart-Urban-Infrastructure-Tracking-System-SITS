from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import (
    onepproject, twopproject, projectcoordinator,
    countryboundery, districtsboundery,
    RoadType, ChainageEvent, RoadAsset, AssetInspection,
)


class ProjectCoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = projectcoordinator
        fields = '__all__'


class OneProjectSerializer(GeoFeatureModelSerializer):
    class Meta:
        geo_field = "oneplocation"
        model = onepproject
        fields = '__all__'


class RoadTypeSerializer(serializers.ModelSerializer):
    code_display = serializers.CharField(source='get_code_display', read_only=True)

    class Meta:
        model = RoadType
        fields = '__all__'


class TwoProjectSerializer(GeoFeatureModelSerializer):
    road_type_detail = RoadTypeSerializer(source='road_type', read_only=True)

    class Meta:
        geo_field = "route"
        model = twopproject
        fields = '__all__'


class ChainageEventSerializer(GeoFeatureModelSerializer):
    event_type_display = serializers.CharField(
        source='get_event_type_display', read_only=True)
    project_name = serializers.CharField(
        source='project.twopname', read_only=True)

    class Meta:
        geo_field = "location"
        model = ChainageEvent
        fields = '__all__'


class RoadAssetSerializer(GeoFeatureModelSerializer):
    asset_type_display = serializers.CharField(
        source='get_asset_type_display', read_only=True)
    condition_display = serializers.CharField(
        source='get_condition_display', read_only=True)
    project_name = serializers.CharField(
        source='project.twopname', read_only=True)

    class Meta:
        geo_field = "location"
        model = RoadAsset
        fields = '__all__'


class AssetInspectionSerializer(serializers.ModelSerializer):
    condition_display = serializers.CharField(
        source='get_condition_display', read_only=True)
    inspected_by_name = serializers.CharField(
        source='inspected_by.coordinatorname', read_only=True,
        default=None)

    class Meta:
        model = AssetInspection
        fields = '__all__'


class CountryBoundarySerializer(GeoFeatureModelSerializer):
    class Meta:
        geo_field = "geom"
        model = countryboundery
        fields = '__all__'


class DistrictBoundarySerializer(GeoFeatureModelSerializer):
    class Meta:
        geo_field = "geom"
        model = districtsboundery
        fields = '__all__'