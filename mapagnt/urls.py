from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('projectcoordinators', views.ProjectCoordinatorViewSet)
router.register('onepprojects', views.OneProjectViewSet)
router.register('twopprojects', views.TwoProjectViewSet)
router.register('road-types', views.RoadTypeViewSet)
router.register('chainage-events', views.ChainageEventViewSet)
router.register('road-assets', views.RoadAssetViewSet)
router.register('asset-inspections', views.AssetInspectionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.homepage, name='home'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("operations/", views.operations, name="operations"),
    path("operationsse/", views.operationsse, name="operationsse"),
    path('create_oneproject/', views.create_onepproject, name='create_oneproject'),
    path('create_twoproject/', views.create_twopproject, name='create_twoproject'),
    path('route/', views.route, name='route'),
    path('fetch_allprojects/', views.fetch_allprojects, name='fetch_allprojects'),
    path('maproute/', views.maproute, name='maproute'),
    path('countrybounderydata/', views.countrybounderydata, name='countrybounderydata'),
    path('districtsbounderydata/', views.districtsbounderydata, name='districtsbounderydata'),
    path('success/', views.successpage, name='successpage'),
    path('updatesuccesspage/', views.updatesuccesspage, name='updatesuccesspage'),

    # New pages
    path('road-assets/', views.road_assets_page, name='road_assets'),
    path('chainage/', views.chainage_page, name='chainage'),

    # Chainage utility endpoints
    path('api/chainage-from-point/<int:project_id>/',
         views.get_chainage_from_point, name='chainage_from_point'),
    path('api/point-from-chainage/<int:project_id>/',
         views.get_point_from_chainage, name='point_from_chainage'),
    path('api/chainage-markers/<int:project_id>/',
         views.generate_chainage_markers, name='chainage_markers'),
]
