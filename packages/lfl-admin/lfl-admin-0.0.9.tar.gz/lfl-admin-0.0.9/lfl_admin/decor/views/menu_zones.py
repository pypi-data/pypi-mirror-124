from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.menu_zones import Menu_zones, Menu_zonesManager


@JsonResponseWithException()
def Menu_zones_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Menu_zones.objects.
                select_related(*get_relation_field_name(model=Menu_zones)).
                get_range_rows1(
                request=request,
                function=Menu_zonesManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zones_Add(request):
    return JsonResponse(DSResponseAdd(data=Menu_zones.objects.createFromRequest(request=request, propsArr=Menu_zonesManager.props(), model=Menu_zones), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zones_Update(request):
    return JsonResponse(DSResponseUpdate(data=Menu_zones.objects.updateFromRequest(request=request, propsArr=Menu_zonesManager.props(), model=Menu_zones), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zones_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Menu_zones.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zones_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Menu_zones.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zones_Info(request):
    return JsonResponse(DSResponse(request=request, data=Menu_zones.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zones_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Menu_zones.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
