from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.news_actions import News_actions, News_actionsManager


@JsonResponseWithException()
def News_actions_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=News_actions.objects.
                select_related(*get_relation_field_name(model=News_actions)).
                get_range_rows1(
                request=request,
                function=News_actionsManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_actions_Add(request):
    return JsonResponse(DSResponseAdd(data=News_actions.objects.createFromRequest(request=request, mdel=News_actions), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_actions_Update(request):
    return JsonResponse(DSResponseUpdate(data=News_actions.objects.updateFromRequest(request=request, model=News_actions), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_actions_Remove(request):
    return JsonResponse(DSResponse(request=request, data=News_actions.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_actions_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=News_actions.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_actions_Info(request):
    return JsonResponse(DSResponse(request=request, data=News_actions.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_actions_Copy(request):
    return JsonResponse(DSResponse(request=request, data=News_actions.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
