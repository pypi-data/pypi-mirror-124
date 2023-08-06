from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.news_action_types import News_action_types, News_action_typesManager


@JsonResponseWithException()
def News_action_types_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=News_action_types.objects.
                select_related(*get_relation_field_name(model=News_action_types)).
                get_range_rows1(
                request=request,
                function=News_action_typesManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_action_types_Add(request):
    return JsonResponse(DSResponseAdd(data=News_action_types.objects.createFromRequest(request=request, propsArr=News_action_typesManager.props(), model=News_action_types), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_action_types_Update(request):
    return JsonResponse(DSResponseUpdate(data=News_action_types.objects.updateFromRequest(request=request, propsArr=News_action_typesManager.props(), model=News_action_types), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_action_types_Remove(request):
    return JsonResponse(DSResponse(request=request, data=News_action_types.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_action_types_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=News_action_types.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_action_types_Info(request):
    return JsonResponse(DSResponse(request=request, data=News_action_types.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_action_types_Copy(request):
    return JsonResponse(DSResponse(request=request, data=News_action_types.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
