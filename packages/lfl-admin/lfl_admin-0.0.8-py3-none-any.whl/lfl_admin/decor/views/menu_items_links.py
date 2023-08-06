from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.menu_items_links import Menu_items_links, Menu_items_linksManager


@JsonResponseWithException()
def Menu_items_links_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Menu_items_links.objects.
                select_related(*get_relation_field_name(model=Menu_items_links)).
                get_range_rows1(
                request=request,
                function=Menu_items_linksManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_links_Add(request):
    return JsonResponse(DSResponseAdd(data=Menu_items_links.objects.createFromRequest(request=request, model=Menu_items_links), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_links_Update(request):
    return JsonResponse(DSResponseUpdate(data=Menu_items_links.objects.updateFromRequest(request=request, model=Menu_items_links), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_links_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items_links.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_links_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items_links.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_links_Info(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items_links.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_links_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items_links.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
