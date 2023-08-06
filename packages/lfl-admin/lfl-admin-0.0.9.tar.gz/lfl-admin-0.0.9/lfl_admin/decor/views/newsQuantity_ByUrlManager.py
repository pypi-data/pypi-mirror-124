from isc_common.common.functions import get_relation_field_name
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from lfl_admin.decor.models.news_quantity_by_url import NewsQuantity_ByUrlManager


@JsonResponseWithException()
def NewsQuantity_ByUrlManager_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=NewsQuantity_ByUrlManager.objects.
                select_related(*get_relation_field_name(model=NewsQuantity_ByUrlManager)).
                get_range_rows1(
                request=request,
                function=NewsQuantity_ByUrlManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def NewsQuantity_ByUrlManager_Add(request):
    return JsonResponse(DSResponseAdd(data=NewsQuantity_ByUrlManager.objects.createFromRequest(request=request, model=NewsQuantity_ByUrlManager), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def NewsQuantity_ByUrlManager_Update(request):
    return JsonResponse(DSResponseUpdate(data=NewsQuantity_ByUrlManager.objects.updateFromRequest(request=request, model=NewsQuantity_ByUrlManager), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def NewsQuantity_ByUrlManager_Remove(request):
    return JsonResponse(DSResponse(request=request, data=NewsQuantity_ByUrlManager.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def NewsQuantity_ByUrlManager_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=NewsQuantity_ByUrlManager.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def NewsQuantity_ByUrlManager_Info(request):
    return JsonResponse(DSResponse(request=request, data=NewsQuantity_ByUrlManager.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def NewsQuantity_ByUrlManager_Copy(request):
    return JsonResponse(DSResponse(request=request, data=NewsQuantity_ByUrlManager.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
