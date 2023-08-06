from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.news_icon_type import News_icon_type, News_icon_typeManager


@JsonResponseWithException()
def News_icon_type_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=News_icon_type.objects.
                select_related(*get_relation_field_name(model=News_icon_type)).
                get_range_rows1(
                request=request,
                function=News_icon_typeManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_icon_type_Add(request):
    return JsonResponse(DSResponseAdd(data=News_icon_type.objects.createFromRequest(request=request, propsArr=News_icon_typeManager.props(), model=News_icon_type), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_icon_type_Update(request):
    return JsonResponse(DSResponseUpdate(data=News_icon_type.objects.updateFromRequest(request=request, propsArr=News_icon_typeManager.props(), model=News_icon_type), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_icon_type_Remove(request):
    return JsonResponse(DSResponse(request=request, data=News_icon_type.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_icon_type_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=News_icon_type.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_icon_type_Info(request):
    return JsonResponse(DSResponse(request=request, data=News_icon_type.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def News_icon_type_Copy(request):
    return JsonResponse(DSResponse(request=request, data=News_icon_type.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
