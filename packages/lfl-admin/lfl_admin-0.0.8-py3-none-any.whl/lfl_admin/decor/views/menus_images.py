from isc_common.common.functions import get_relation_field_name
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from lfl_admin.decor.models.menus_images import Menus_images, Menus_imagesManager


@JsonResponseWithException()
def Menus_images_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Menus_images.objects.
                select_related(*get_relation_field_name(model=Menus_images)).
                get_range_rows1(
                request=request,
                function=Menus_imagesManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menus_images_Add(request):
    return JsonResponse(DSResponseAdd(data=Menus_images.objects.createFromRequest(request=request, model=Menus_images), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menus_images_Update(request):
    return JsonResponse(DSResponseUpdate(data=Menus_images.objects.updateFromRequest(request=request, model=Menus_images), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menus_images_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Menus_images.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menus_images_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Menus_images.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menus_images_Info(request):
    return JsonResponse(DSResponse(request=request, data=Menus_images.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menus_images_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Menus_images.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
