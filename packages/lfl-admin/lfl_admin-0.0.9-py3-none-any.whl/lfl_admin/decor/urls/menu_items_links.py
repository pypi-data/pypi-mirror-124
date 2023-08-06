from django.urls import path

from lfl_admin.decor.views import menu_items_links

urlpatterns = [

    path('Menu_items_links/Fetch/', menu_items_links.Menu_items_links_Fetch),
    path('Menu_items_links/Add', menu_items_links.Menu_items_links_Add),
    path('Menu_items_links/Update', menu_items_links.Menu_items_links_Update),
    path('Menu_items_links/Remove', menu_items_links.Menu_items_links_Remove),
    path('Menu_items_links/Lookup/', menu_items_links.Menu_items_links_Lookup),
    path('Menu_items_links/Info/', menu_items_links.Menu_items_links_Info),
    path('Menu_items_links/Copy', menu_items_links.Menu_items_links_Copy),

]
