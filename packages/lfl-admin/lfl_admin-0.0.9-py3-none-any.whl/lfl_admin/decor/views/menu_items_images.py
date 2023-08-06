from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.decor.models.menu_items_images import Menu_items_images, Menu_items_imagesManager


@JsonResponseWithException()
def Menu_items_images_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Menu_items_images.objects.
                select_related(*get_relation_field_name(model=Menu_items_images)).
                get_range_rows1(
                request=request,
                function=Menu_items_imagesManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_images_Add(request):
    return JsonResponse(DSResponseAdd(data=Menu_items_images.objects.createFromRequest(request=request, model=Menu_items_images), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_images_Update(request):
    return JsonResponse(DSResponseUpdate(data=Menu_items_images.objects.updateFromRequest(request=request, model=Menu_items_images), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_images_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items_images.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_images_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items_images.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_images_Info(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items_images.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Menu_items_images_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Menu_items_images.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
