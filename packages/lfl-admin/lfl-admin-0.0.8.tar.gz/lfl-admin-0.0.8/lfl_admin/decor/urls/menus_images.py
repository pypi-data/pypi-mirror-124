from django.urls import path
from lfl_admin.decor.views import menus_images

urlpatterns = [

    path('Menus_images/Fetch/', menus_images.Menus_images_Fetch),
    path('Menus_images/Add', menus_images.Menus_images_Add),
    path('Menus_images/Update', menus_images.Menus_images_Update),
    path('Menus_images/Remove', menus_images.Menus_images_Remove),
    path('Menus_images/Lookup/', menus_images.Menus_images_Lookup),
    path('Menus_images/Info/', menus_images.Menus_images_Info),
    path('Menus_images/Copy', menus_images.Menus_images_Copy),

]
