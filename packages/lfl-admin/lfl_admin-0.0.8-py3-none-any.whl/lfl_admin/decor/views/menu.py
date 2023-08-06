from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.menu import Menu, MenuManager


@JsonResponseWithException()
def Menu_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Menu.objects.
                select_related(*get_relation_field_name(model=Menu)).
                get_range_rows1(
                request=request,
                function=MenuManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_Add(request):
    return JsonResponse(DSResponseAdd(data=Menu.objects.createFromRequest(request=request, propsArr=MenuManager.props(), model=Menu), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_Update(request):
    return JsonResponse(DSResponseUpdate(data=Menu.objects.updateFromRequest(request=request, propsArr=MenuManager.props(), model=Menu), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Menu.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Menu.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_Info(request):
    return JsonResponse(DSResponse(request=request, data=Menu.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Menu.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
