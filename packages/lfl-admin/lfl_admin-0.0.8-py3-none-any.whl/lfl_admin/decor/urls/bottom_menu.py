from django.urls import path

from lfl_admin.decor.views import bottom_menu

urlpatterns = [

    path('Bottom_menu/Fetch/', bottom_menu.Bottom_menu_Fetch),
    path('Bottom_menu/Add', bottom_menu.Bottom_menu_Add),
    path('Bottom_menu/Update', bottom_menu.Bottom_menu_Update),
    path('Bottom_menu/Remove', bottom_menu.Bottom_menu_Remove),
    path('Bottom_menu/Lookup/', bottom_menu.Bottom_menu_Lookup),
    path('Bottom_menu/Info/', bottom_menu.Bottom_menu_Info),
    path('Bottom_menu/Copy', bottom_menu.Bottom_menu_Copy),

]
