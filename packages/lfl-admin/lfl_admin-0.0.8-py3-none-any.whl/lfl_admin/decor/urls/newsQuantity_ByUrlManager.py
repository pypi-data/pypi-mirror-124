from django.urls import path
from lfl_admin.decor.views import newsQuantity_ByUrlManager

urlpatterns = [

    path('NewsQuantity_ByUrlManager/Fetch/', newsQuantity_ByUrlManager.NewsQuantity_ByUrlManager_Fetch),
    path('NewsQuantity_ByUrlManager/Add', newsQuantity_ByUrlManager.NewsQuantity_ByUrlManager_Add),
    path('NewsQuantity_ByUrlManager/Update', newsQuantity_ByUrlManager.NewsQuantity_ByUrlManager_Update),
    path('NewsQuantity_ByUrlManager/Remove', newsQuantity_ByUrlManager.NewsQuantity_ByUrlManager_Remove),
    path('NewsQuantity_ByUrlManager/Lookup/', newsQuantity_ByUrlManager.NewsQuantity_ByUrlManager_Lookup),
    path('NewsQuantity_ByUrlManager/Info/', newsQuantity_ByUrlManager.NewsQuantity_ByUrlManager_Info),
    path('NewsQuantity_ByUrlManager/Copy', newsQuantity_ByUrlManager.NewsQuantity_ByUrlManager_Copy),

]
