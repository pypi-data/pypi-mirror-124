from django.urls import path

from lfl_admin.decor.views import menu_zone_types

urlpatterns = [

    path('Menu_zone_types/Fetch/', menu_zone_types.Menu_zone_types_Fetch),
    path('Menu_zone_types/Add', menu_zone_types.Menu_zone_types_Add),
    path('Menu_zone_types/Update', menu_zone_types.Menu_zone_types_Update),
    path('Menu_zone_types/Remove', menu_zone_types.Menu_zone_types_Remove),
    path('Menu_zone_types/Lookup/', menu_zone_types.Menu_zone_types_Lookup),
    path('Menu_zone_types/Info/', menu_zone_types.Menu_zone_types_Info),
    path('Menu_zone_types/Copy', menu_zone_types.Menu_zone_types_Copy),

]
