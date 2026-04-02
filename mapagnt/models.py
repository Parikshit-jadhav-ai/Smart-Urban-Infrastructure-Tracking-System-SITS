from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.gis.db.models import MultiPolygonField
from django.db.models import Manager as GeoManager


class projectcoordinator(models.Model):
    PROJECT_COORDINATOR = [
        ('projectmanager', 'Project Manager'),
        ("seniorcivilengineer", "Sr. Civil Engineer"),
        ("juniorcivilengineer", "Jr. Civil Engineer"),
        ('siteengineer', 'Site Engineer'),
        ('labourcoordinator', 'Labour Coordinator'),
    ]
    coordinatorname = models.CharField(max_length=100)
    coordinatordesignation = models.CharField(max_length=100, choices=PROJECT_COORDINATOR)
    coordinatoremail = models.EmailField()
    coordinatorphnumber = models.CharField(max_length=15)
    coordinatoraddress = models.CharField(max_length=200)
    coordinatorzip_code = models.CharField(max_length=20)
    coordinatorcity = models.CharField(max_length=100)
    coordinatorstate = models.CharField(max_length=100)

    def __str__(self):
        return self.coordinatorname


class onepproject(models.Model):
    ONEPROJECT_TYPES = [
        ('municipalfacility', 'Municipal Facility'),
        ('governmentfacility', 'Government Facility'),
        ('communityfacilities', 'Community Facilities'),
        ('policestation', 'Police Station'),
        ('parkandgardens', 'Park and Gardens'),
    ]
    ONEPROJECT_STATUS_CHOICES = [
        ("design", "Design"),
        ('inProgress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    onepname = models.CharField(max_length=100)
    oneptype = models.CharField(max_length=50, choices=ONEPROJECT_TYPES)
    onepbudget = models.DecimalField(max_digits=17, decimal_places=2)
    onepstatus = models.CharField(max_length=20, choices=ONEPROJECT_STATUS_CHOICES)
    onecoordinatorname = models.CharField(max_length=100, null=True)
    onepdescription = models.CharField(max_length=200)
    onepaddress = models.CharField(max_length=200, null=True)
    oneplatitude = models.DecimalField(max_digits=9, decimal_places=6)
    oneplongitude = models.DecimalField(max_digits=9, decimal_places=6)
    oneplocation = models.PointField(blank=True, null=True, srid=4326)
    objects = GeoManager()

    def __str__(self):
        return str(self.onepname)

    class Meta:
        verbose_name_plural = "oneppmodel"


# ─── Road Type Classification ────────────────────────────────────────────────

class RoadType(models.Model):
    """Road classification: NH, SH, MDR, ODR, VR, etc."""
    ROAD_TYPE_CODES = [
        ('NH', 'National Highway'),
        ('SH', 'State Highway'),
        ('MDR', 'Major District Road'),
        ('ODR', 'Other District Road'),
        ('VR', 'Village Road'),
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, choices=ROAD_TYPE_CODES, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default='gray',
                             help_text="Map display color, e.g. red, #FF5500")
    weight = models.IntegerField(default=3,
                                 help_text="Map line weight in pixels")

    def __str__(self):
        return f"{self.get_code_display()} ({self.code})"

    class Meta:
        verbose_name_plural = "Road Types"


# ─── Two-Point Project (updated with route/chainage/road-type) ────────────────

class twopproject(models.Model):
    TWOPROJECT_TYPES = [
        ('pipeline', 'Pipe Line'),
        ('highwayconstruction', 'Highway Construction'),
        ('roadrehabilitation', 'Road Rehabilitation'),
        ('drainagerehabilitation', 'Drainage Rehabilitation'),
        ('bridgesandtunnels', 'Bridges and Tunnels'),
    ]
    TWOPROJECT_STATUS_CHOICES = [
        ("design", "Design"),
        ('inProgress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    twopname = models.CharField(max_length=100)
    twoptype = models.CharField(max_length=50, choices=TWOPROJECT_TYPES)
    twopbudget = models.DecimalField(max_digits=17, decimal_places=2)
    twopstatus = models.CharField(max_length=20, choices=TWOPROJECT_STATUS_CHOICES)
    twocoordinatorname = models.CharField(max_length=100, null=True)
    twopdescription = models.CharField(max_length=200)
    twopaddress = models.CharField(max_length=200, null=True)

    # Legacy start/end points (kept for backward compatibility)
    twopstartlat = models.DecimalField(max_digits=9, decimal_places=6)
    twopstartlon = models.DecimalField(max_digits=9, decimal_places=6)
    twopstart_point = models.PointField(blank=True, null=True, srid=4326)
    twopendlat = models.DecimalField(max_digits=9, decimal_places=6)
    twopendlon = models.DecimalField(max_digits=9, decimal_places=6)
    twopend_point = models.PointField(blank=True, null=True, srid=4326)

    # ── New: Route geometry & chainage ──
    route = models.LineStringField(blank=True, null=True, srid=4326,
                                   help_text="Full route geometry as LineString")
    start_chainage = models.FloatField(default=0,
                                       help_text="Start chainage in meters")
    end_chainage = models.FloatField(null=True, blank=True,
                                     help_text="End chainage in meters")

    # ── New: Road type classification ──
    road_type = models.ForeignKey(RoadType, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='projects')
    carriageway_width = models.FloatField(null=True, blank=True,
                                          help_text="Width in meters")
    lanes = models.IntegerField(default=2)

    objects = GeoManager()

    def __str__(self):
        return str(self.twopname)

    class Meta:
        verbose_name_plural = "twopproject"


# ─── Chainage Events ─────────────────────────────────────────────────────────

class ChainageEvent(models.Model):
    """An event or point-of-interest at a specific chainage along a road."""
    EVENT_TYPES = [
        ('milestone', 'Milestone'),
        ('intersection', 'Intersection'),
        ('tollbooth', 'Toll Booth'),
        ('restarea', 'Rest Area'),
        ('accident_zone', 'Accident Zone'),
        ('construction', 'Construction Zone'),
        ('other', 'Other'),
    ]
    project = models.ForeignKey(twopproject, on_delete=models.CASCADE,
                                related_name='chainage_events')
    chainage = models.FloatField(help_text="Distance along route in meters")
    location = models.PointField(srid=4326,
                                 help_text="Geographic point at this chainage")
    event_type = models.CharField(max_length=100, choices=EVENT_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = GeoManager()

    def __str__(self):
        return f"{self.get_event_type_display()} @ {self.chainage}m — {self.project}"

    class Meta:
        ordering = ['chainage']
        verbose_name_plural = "Chainage Events"


# ─── Road Assets ──────────────────────────────────────────────────────────────

class RoadAsset(models.Model):
    """A physical asset located along a road."""
    ASSET_TYPES = [
        ('pole', 'Electric Pole'),
        ('sign', 'Sign Board'),
        ('drain', 'Drain'),
        ('bridge', 'Bridge'),
        ('culvert', 'Culvert'),
        ('traffic_signal', 'Traffic Signal'),
        ('streetlight', 'Street Light'),
        ('guardrail', 'Guard Rail'),
    ]
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('moderate', 'Moderate'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]
    project = models.ForeignKey(twopproject, on_delete=models.CASCADE,
                                related_name='road_assets')
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    location = models.PointField(srid=4326)
    chainage = models.FloatField(help_text="Chainage along the road in meters")
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES,
                                 default='good')
    installation_date = models.DateField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True,
                                help_text="Extra attributes as JSON")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = GeoManager()

    def __str__(self):
        return f"{self.get_asset_type_display()} @ {self.chainage}m — {self.project}"

    class Meta:
        ordering = ['chainage']
        verbose_name_plural = "Road Assets"


# ─── Asset Inspections ────────────────────────────────────────────────────────

class AssetInspection(models.Model):
    """An inspection record for a road asset."""
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('moderate', 'Moderate'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]
    asset = models.ForeignKey(RoadAsset, on_delete=models.CASCADE,
                              related_name='inspections')
    inspection_date = models.DateField()
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    remarks = models.TextField(blank=True)
    inspected_by = models.ForeignKey(projectcoordinator,
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection of {self.asset} on {self.inspection_date}"

    class Meta:
        ordering = ['-inspection_date']
        verbose_name_plural = "Asset Inspections"


# ─── Boundary models (unchanged) ─────────────────────────────────────────────

class countryboundery(models.Model):
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=20)
    geom = MultiPolygonField(srid=4326)

    def __unicode__(self):
        return self.name


class districtsboundery(models.Model):
    dist_name = models.CharField(max_length=30)
    state_name = models.CharField(max_length=50)
    geom = MultiPolygonField(srid=4326)

    def __unicode__(self):
        return self.dist_name