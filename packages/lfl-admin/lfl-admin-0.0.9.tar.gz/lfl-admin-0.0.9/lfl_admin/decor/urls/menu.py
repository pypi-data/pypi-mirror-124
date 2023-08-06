from django.urls import path

from lfl_admin.decor.views import menu

urlpatterns = [

    path('Menu/Fetch/', menu.Menu_Fetch),
    path('Menu/Add', menu.Menu_Add),
    path('Menu/Update', menu.Menu_Update),
    path('Menu/Remove', menu.Menu_Remove),
    path('Menu/Lookup/', menu.Menu_Lookup),
    path('Menu/Info/', menu.Menu_Info),
    path('Menu/Copy', menu.Menu_Copy),

]
