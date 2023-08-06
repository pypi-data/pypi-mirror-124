from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.menu_item_leagues import Menu_item_leagues, Menu_item_leaguesManager


@JsonResponseWithException()
def Menu_item_leagues_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Menu_item_leagues.objects.
                select_related(*get_relation_field_name(model=Menu_item_leagues)).
                get_range_rows1(
                request=request,
                function=Menu_item_leaguesManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_item_leagues_Add(request):
    return JsonResponse(DSResponseAdd(data=Menu_item_leagues.objects.createFromRequest(request=request, propsArr=Menu_item_leaguesManager.props(), model=Menu_item_leagues), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_item_leagues_Update(request):
    return JsonResponse(DSResponseUpdate(data=Menu_item_leagues.objects.updateFromRequest(request=request, propsArr=Menu_item_leaguesManager.props(), model=Menu_item_leagues), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_item_leagues_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Menu_item_leagues.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_item_leagues_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Menu_item_leagues.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_item_leagues_Info(request):
    return JsonResponse(DSResponse(request=request, data=Menu_item_leagues.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_item_leagues_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Menu_item_leagues.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
