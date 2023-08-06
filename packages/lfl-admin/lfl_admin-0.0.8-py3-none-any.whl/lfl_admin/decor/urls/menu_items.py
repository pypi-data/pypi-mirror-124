from django.urls import path

from lfl_admin.decor.views import menu_items

urlpatterns = [

    path('Menu_items/Fetch/', menu_items.Menu_items_Fetch),
    path('Menu_items/Add', menu_items.Menu_items_Add),
    path('Menu_items/Update', menu_items.Menu_items_Update),
    path('Menu_items/Remove', menu_items.Menu_items_Remove),
    path('Menu_items/Lookup/', menu_items.Menu_items_Lookup),
    path('Menu_items/Info/', menu_items.Menu_items_Info),
    path('Menu_items/Copy', menu_items.Menu_items_Copy),

]
