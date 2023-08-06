from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from lfl_admin.competitions.models.squads_text_informations import Squads_text_informations , Squads_text_informationsManager


@JsonResponseWithException()
def Squads_text_informations_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Squads_text_informations.objects.
                select_related().
                get_range_rows1(
                request=request ,
                function=Squads_text_informationsManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Squads_text_informations_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Squads_text_informations.objects.createFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Squads_text_informations_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Squads_text_informations.objects.updateFromRequest( request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Squads_text_informations_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Squads_text_informations.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Squads_text_informations_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Squads_text_informations.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Squads_text_informations_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Squads_text_informations.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Squads_text_informations_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Squads_text_informations.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )
