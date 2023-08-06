from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.news_start_block_tournament_links import News_start_block_tournament_links, News_start_block_tournament_linksManager


@JsonResponseWithException()
def News_start_block_tournament_links_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=News_start_block_tournament_links.objects.
                select_related(*get_relation_field_name(model=News_start_block_tournament_links)).
                get_range_rows1(
                request=request,
                function=News_start_block_tournament_linksManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_start_block_tournament_links_Add(request):
    return JsonResponse(DSResponseAdd(data=News_start_block_tournament_links.objects.createFromRequest(request=request, model=News_start_block_tournament_links), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_start_block_tournament_links_Update(request):
    return JsonResponse(DSResponseUpdate(data=News_start_block_tournament_links.objects.updateFromRequest(request=request, model=News_start_block_tournament_links), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_start_block_tournament_links_Remove(request):
    return JsonResponse(DSResponse(request=request, data=News_start_block_tournament_links.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_start_block_tournament_links_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=News_start_block_tournament_links.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_start_block_tournament_links_Info(request):
    return JsonResponse(DSResponse(request=request, data=News_start_block_tournament_links.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_start_block_tournament_links_Copy(request):
    return JsonResponse(DSResponse(request=request, data=News_start_block_tournament_links.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
