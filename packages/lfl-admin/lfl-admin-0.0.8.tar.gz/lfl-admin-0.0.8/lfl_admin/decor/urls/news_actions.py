from django.urls import path

from lfl_admin.decor.views import news_actions

urlpatterns = [

    path('News_actions/Fetch/', news_actions.News_actions_Fetch),
    path('News_actions/Add', news_actions.News_actions_Add),
    path('News_actions/Update', news_actions.News_actions_Update),
    path('News_actions/Remove', news_actions.News_actions_Remove),
    path('News_actions/Lookup/', news_actions.News_actions_Lookup),
    path('News_actions/Info/', news_actions.News_actions_Info),
    path('News_actions/Copy', news_actions.News_actions_Copy),

]
