from django.urls import path

from lfl_admin.decor.views import menu_item_leagues

urlpatterns = [

    path('Menu_item_leagues/Fetch/', menu_item_leagues.Menu_item_leagues_Fetch),
    path('Menu_item_leagues/Add', menu_item_leagues.Menu_item_leagues_Add),
    path('Menu_item_leagues/Update', menu_item_leagues.Menu_item_leagues_Update),
    path('Menu_item_leagues/Remove', menu_item_leagues.Menu_item_leagues_Remove),
    path('Menu_item_leagues/Lookup/', menu_item_leagues.Menu_item_leagues_Lookup),
    path('Menu_item_leagues/Info/', menu_item_leagues.Menu_item_leagues_Info),
    path('Menu_item_leagues/Copy', menu_item_leagues.Menu_item_leagues_Copy),

]
