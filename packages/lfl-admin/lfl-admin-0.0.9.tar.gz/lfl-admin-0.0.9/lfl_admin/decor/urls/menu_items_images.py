from django.urls import path

from lfl_admin.decor.views import menu_items_images

urlpatterns = [

    path('Menu_items_images/Fetch/', menu_items_images.Menu_items_images_Fetch),
    path('Menu_items_images/Add', menu_items_images.Menu_items_images_Add),
    path('Menu_items_images/Update', menu_items_images.Menu_items_images_Update),
    path('Menu_items_images/Remove', menu_items_images.Menu_items_images_Remove),
    path('Menu_items_images/Lookup/', menu_items_images.Menu_items_images_Lookup),
    path('Menu_items_images/Info/', menu_items_images.Menu_items_images_Info),
    path('Menu_items_images/Copy', menu_items_images.Menu_items_images_Copy),

]
