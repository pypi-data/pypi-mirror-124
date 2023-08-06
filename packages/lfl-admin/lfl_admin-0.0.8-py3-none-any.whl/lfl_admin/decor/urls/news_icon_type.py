from django.urls import path

from lfl_admin.decor.views import news_icon_type

urlpatterns = [

    path('News_icon_type/Fetch/', news_icon_type.News_icon_type_Fetch),
    path('News_icon_type/Add', news_icon_type.News_icon_type_Add),
    path('News_icon_type/Update', news_icon_type.News_icon_type_Update),
    path('News_icon_type/Remove', news_icon_type.News_icon_type_Remove),
    path('News_icon_type/Lookup/', news_icon_type.News_icon_type_Lookup),
    path('News_icon_type/Info/', news_icon_type.News_icon_type_Info),
    path('News_icon_type/Copy', news_icon_type.News_icon_type_Copy),

]
