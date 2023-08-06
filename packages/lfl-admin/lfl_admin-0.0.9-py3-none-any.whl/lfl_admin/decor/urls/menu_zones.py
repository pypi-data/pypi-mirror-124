from django.urls import path

from lfl_admin.decor.views import menu_zones

urlpatterns = [

    path('Menu_zones/Fetch/', menu_zones.Menu_zones_Fetch),
    path('Menu_zones/Add', menu_zones.Menu_zones_Add),
    path('Menu_zones/Update', menu_zones.Menu_zones_Update),
    path('Menu_zones/Remove', menu_zones.Menu_zones_Remove),
    path('Menu_zones/Lookup/', menu_zones.Menu_zones_Lookup),
    path('Menu_zones/Info/', menu_zones.Menu_zones_Info),
    path('Menu_zones/Copy', menu_zones.Menu_zones_Copy),

]
