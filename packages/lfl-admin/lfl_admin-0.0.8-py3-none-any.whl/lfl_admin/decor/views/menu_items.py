from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.menu_items import Menu_items, Menu_itemsManager


@JsonResponseWithException()
def Menu_items_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Menu_items.objects.
                select_related(*get_relation_field_name(model=Menu_items)).
                get_range_rows1(
                request=request,
                function=Menu_itemsManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_Add(request):
    return JsonResponse(DSResponseAdd(data=Menu_items.objects.createFromRequest(request=request, model=Menu_items), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_Update(request):
    return JsonResponse(DSResponseUpdate(data=Menu_items.objects.updateFromRequest(request=request, model=Menu_items), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_Info(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
