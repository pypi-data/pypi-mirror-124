class GridCoonstant :
    refresh_command_structure_view_grid = "refresh_command_structure_view_grid"
    refresh_command_structure_view_grid_row = "refresh_command_structure_view_grid_row"


def make_interregion( apps , schema_editor ) :
    from isc_common.common import unknown_name
    from isc_common.common import unknown
    from django.db import transaction
    from lfl_admin.region.models.interregion import Interregion

    def interregion_2_code_name( interregion ) :
        if interregion is None :
            name = unknown_name
            code = unknown
        elif interregion == '1' :
            name = 'Москва'
            code = interregion
        elif interregion == '2' :
            name = 'Мир'
            code = interregion
        elif interregion == '3' :
            name = 'Поволжье'
            code = interregion
        elif interregion == '4' :
            name = 'Юг'
            code = interregion
        elif interregion == '5' :
            name = 'Мир'
            code = interregion
        elif interregion == '6' :
            name = 'Москва и Поволжье'
            code = interregion
        elif interregion == '7' :
            name = 'Москва и Юг'
            code = interregion
        elif interregion == '8' :
            name = 'Санкт-Петербург'
            code = interregion
        elif interregion == '9' :
            name = 'Центр'
            code = interregion
        elif interregion == '10' :
            name = 'Восток'
            code = interregion
        elif interregion == '11' :
            name = 'Черноземье'
            code = interregion
        elif interregion == '12' :
            name = 'Крым'
            code = interregion
        else :
            name = unknown_name
            code = unknown

        return code , name

    from lfl_admin.competitions.models.clubs import Clubs
    from tqdm import tqdm

    query = Clubs.objects.exclude( interregion=None )
    pbar = tqdm( total=query.count() )

    with transaction.atomic() :
        for i in range( 13 ) :
            code , name = interregion_2_code_name( str( i ) )
            interregion , _ = Interregion.objects.get_or_create( code=code , defaults=dict( name=name ) )

        for club in query :
            code , name = interregion_2_code_name( club.interregion )
            interregion , _ = Interregion.objects.get_or_create( code=code , defaults=dict( name=name ) )
            club.interregion1 = interregion
            club.save()
            pbar.update()
