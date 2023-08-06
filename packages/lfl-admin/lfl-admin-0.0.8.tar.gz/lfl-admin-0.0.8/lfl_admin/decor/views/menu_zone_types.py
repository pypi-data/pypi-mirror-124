from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.menu_zone_types import Menu_zone_types, Menu_zone_typesManager


@JsonResponseWithException()
def Menu_zone_types_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Menu_zone_types.objects.
                select_related(*get_relation_field_name(model=Menu_zone_types)).
                get_range_rows1(
                request=request,
                function=Menu_zone_typesManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zone_types_Add(request):
    return JsonResponse(DSResponseAdd(data=Menu_zone_types.objects.createFromRequest(request=request, propsArr=Menu_zone_typesManager.props(), model=Menu_zone_types), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zone_types_Update(request):
    return JsonResponse(DSResponseUpdate(data=Menu_zone_types.objects.updateFromRequest(request=request, propsArr=Menu_zone_typesManager.props(), model=Menu_zone_types), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zone_types_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Menu_zone_types.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zone_types_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Menu_zone_types.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zone_types_Info(request):
    return JsonResponse(DSResponse(request=request, data=Menu_zone_types.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_zone_types_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Menu_zone_types.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
