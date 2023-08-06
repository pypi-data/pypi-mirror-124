from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from lfl_admin.votes.models.polls_text_informations import Polls_text_informationsManager, Polls_text_informations


@JsonResponseWithException()
def Polls_text_informations_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Polls_text_informations.objects.
                select_related().
                get_range_rows1(
                request=request,
                function=Polls_text_informationsManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Polls_text_informations_Add(request):
    return JsonResponse(DSResponseAdd(data=Polls_text_informations.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Polls_text_informations_Update(request):
    return JsonResponse(DSResponseUpdate(data=Polls_text_informations.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Polls_text_informations_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Polls_text_informations.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Polls_text_informations_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Polls_text_informations.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Polls_text_informations_Info(request):
    return JsonResponse(DSResponse(request=request, data=Polls_text_informations.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Polls_text_informations_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Polls_text_informations.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
