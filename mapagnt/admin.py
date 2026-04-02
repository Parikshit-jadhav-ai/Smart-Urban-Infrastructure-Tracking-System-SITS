from django.contrib import admin
from .models import (
    onepproject, twopproject, projectcoordinator,
    countryboundery, districtsboundery,
    RoadType, ChainageEvent, RoadAsset, AssetInspection,
)
from leaflet.admin import LeafletGeoAdmin


# ─── Existing admin panels ───────────────────────────────────────────────────

class projectcoordinatorpanal(LeafletGeoAdmin):
    list_display = (
        "coordinatorname", "coordinatordesignation", "coordinatorphnumber",
        "coordinatoraddress", "coordinatorcity", "coordinatorzip_code",
        "coordinatorcity", "coordinatorstate",
    )


class onepprojectpanel(LeafletGeoAdmin):
    list_display = (
        "onepname", "oneptype", "onepbudget", "onepstatus",
        "onecoordinatorname", "onepdescription", "onepaddress",
        "oneplatitude", "oneplongitude", "oneplocation",
    )


class twopprojectpanel(LeafletGeoAdmin):
    list_display = (
        "twopname", "twoptype", "twopbudget", "twopstatus",
        "twocoordinatorname", "twopdescription", "twopaddress",
        "twopstartlat", "twopstartlon", "twopstart_point",
        "twopendlat", "twopendlon", "twopend_point",
        "road_type", "lanes", "carriageway_width",
    )
    list_filter = ("twoptype", "twopstatus", "road_type")
    search_fields = ("twopname",)


class countrymapmakerpanel(LeafletGeoAdmin):
    list_display = ("name", "type")


class districtsbounderypanel(LeafletGeoAdmin):
    list_display = ("dist_name", "state_name")


# ─── New admin panels ────────────────────────────────────────────────────────

class RoadTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "color", "weight")
    search_fields = ("name", "code")


class ChainageEventAdmin(LeafletGeoAdmin):
    list_display = ("project", "chainage", "event_type", "created_at")
    list_filter = ("event_type",)
    search_fields = ("project__twopname", "description")


class RoadAssetAdmin(LeafletGeoAdmin):
    list_display = (
        "project", "asset_type", "chainage", "condition",
        "installation_date", "created_at",
    )
    list_filter = ("asset_type", "condition")
    search_fields = ("project__twopname",)


class AssetInspectionAdmin(admin.ModelAdmin):
    list_display = (
        "asset", "inspection_date", "condition",
        "inspected_by", "created_at",
    )
    list_filter = ("condition", "inspection_date")
    search_fields = ("asset__project__twopname", "remarks")


# ─── Register all models ─────────────────────────────────────────────────────

admin.site.register(projectcoordinator, LeafletGeoAdmin)
admin.site.register(onepproject, LeafletGeoAdmin)
admin.site.register(twopproject, twopprojectpanel)
admin.site.register(countryboundery, LeafletGeoAdmin)
admin.site.register(districtsboundery, LeafletGeoAdmin)

admin.site.register(RoadType, RoadTypeAdmin)
admin.site.register(ChainageEvent, ChainageEventAdmin)
admin.site.register(RoadAsset, RoadAssetAdmin)
admin.site.register(AssetInspection, AssetInspectionAdmin)
