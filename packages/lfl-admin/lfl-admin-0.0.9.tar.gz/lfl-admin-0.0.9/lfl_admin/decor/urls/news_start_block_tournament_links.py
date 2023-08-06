from django.urls import path

from lfl_admin.decor.views import news_start_block_tournament_links

urlpatterns = [

    path('News_start_block_tournament_links/Fetch/', news_start_block_tournament_links.News_start_block_tournament_links_Fetch),
    path('News_start_block_tournament_links/Add', news_start_block_tournament_links.News_start_block_tournament_links_Add),
    path('News_start_block_tournament_links/Update', news_start_block_tournament_links.News_start_block_tournament_links_Update),
    path('News_start_block_tournament_links/Remove', news_start_block_tournament_links.News_start_block_tournament_links_Remove),
    path('News_start_block_tournament_links/Lookup/', news_start_block_tournament_links.News_start_block_tournament_links_Lookup),
    path('News_start_block_tournament_links/Info/', news_start_block_tournament_links.News_start_block_tournament_links_Info),
    path('News_start_block_tournament_links/Copy', news_start_block_tournament_links.News_start_block_tournament_links_Copy),

]
