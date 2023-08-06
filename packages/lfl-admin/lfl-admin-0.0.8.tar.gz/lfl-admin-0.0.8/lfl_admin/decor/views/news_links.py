from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from lfl_admin.decor.models.news_links import News_links, News_linksManager


@JsonResponseWithException()
def News_links_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=News_links.objects.
                select_related().
                get_range_rows1(
                request=request,
                function=News_linksManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_links_Add(request):
    return JsonResponse(DSResponseAdd(data=News_links.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_links_Update(request):
    return JsonResponse(DSResponseUpdate(data=News_links.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_links_Remove(request):
    return JsonResponse(DSResponse(request=request, data=News_links.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_links_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=News_links.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_links_Info(request):
    return JsonResponse(DSResponse(request=request, data=News_links.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_links_Copy(request):
    return JsonResponse(DSResponse(request=request, data=News_links.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
