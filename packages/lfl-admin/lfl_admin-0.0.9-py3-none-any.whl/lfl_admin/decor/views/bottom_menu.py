from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.bottom_menu import Bottom_menu, Bottom_menuManager


@JsonResponseWithException()
def Bottom_menu_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Bottom_menu.objects.
                select_related(*get_relation_field_name(model=Bottom_menu)).
                get_range_rows1(
                request=request,
                function=Bottom_menuManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Bottom_menu_Add(request):
    return JsonResponse(DSResponseAdd(data=Bottom_menu.objects.createFromRequest(request=request, model=Bottom_menu), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Bottom_menu_Update(request):
    return JsonResponse(DSResponseUpdate(data=Bottom_menu.objects.updateFromRequest(request=request, model=Bottom_menu), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Bottom_menu_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Bottom_menu.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Bottom_menu_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Bottom_menu.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Bottom_menu_Info(request):
    return JsonResponse(DSResponse(request=request, data=Bottom_menu.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Bottom_menu_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Bottom_menu.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
