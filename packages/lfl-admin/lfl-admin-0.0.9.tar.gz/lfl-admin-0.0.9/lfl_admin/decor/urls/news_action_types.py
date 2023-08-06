from django.urls import path

from lfl_admin.decor.views import news_action_types

urlpatterns = [

    path('News_action_types/Fetch/', news_action_types.News_action_types_Fetch),
    path('News_action_types/Add', news_action_types.News_action_types_Add),
    path('News_action_types/Update', news_action_types.News_action_types_Update),
    path('News_action_types/Remove', news_action_types.News_action_types_Remove),
    path('News_action_types/Lookup/', news_action_types.News_action_types_Lookup),
    path('News_action_types/Info/', news_action_types.News_action_types_Info),
    path('News_action_types/Copy', news_action_types.News_action_types_Copy),

]
