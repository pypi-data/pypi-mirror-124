import logging

from django.core.management import BaseCommand
from django.db import transaction
from isc_common.common import unknown
from tqdm import tqdm

from lfl_admin.competitions.models.disqualification_condition import Disqualification_condition
from lfl_admin.competitions.models.disqualification_zones import Disqualification_zones
from lfl_admin.competitions.models.division_stages import Division_stages
from lfl_admin.competitions.models.divisions import Divisions
from lfl_admin.competitions.models.tournaments import Tournaments
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger( __name__ )


def restruct_divisions() :
    with transaction.atomic() :
        pbar = tqdm( total=Tournaments.objects.filter( division_id__in=map( lambda x : x.id , Divisions.objects.filter( parent=None ) ) ).exclude( division__code=unknown ).count() )

        for division in Divisions.objects.filter( parent=None ).exclude( code=unknown ) :
            for tournament in Tournaments.objects.filter( division=division ) :
                # print(tournament.division_round)
                stage , _ = Division_stages.objects.get_or_create( code=tournament.division_round if tournament.division_round else 0 , defaults=dict( name=f'Этап: {tournament.division_round}' ) )

                props = 0
                props_t = tournament.props

                if division.props.active.is_set :
                    props |= Divisions.props.active
                    props_t |= Tournaments.props.active
                else :
                    props &= ~Divisions.props.active
                    props_t &= ~ Tournaments.props.active

                if division.props.completed.is_set :
                    props |= Divisions.props.completed
                    props_t &= ~Tournaments.props.active

                if division.props.favorites.is_set :
                    props |= Divisions.props.favorites
                    props_t |= Tournaments.props.favorites
                else :
                    props &= ~ Divisions.props.favorites
                    props_t &= ~ Tournaments.props.favorites

                if division.props.hidden.is_set :
                    props_t |= Tournaments.props.favorites
                    props |= Divisions.props.hidden
                else :
                    props_t &= ~ Tournaments.props.favorites
                    props &= ~ Divisions.props.hidden

                division_stage , _ = Divisions.objects.get_or_create(
                    stage=stage ,
                    parent=division ,
                    defaults=dict(
                        name=stage.name ,
                        disqualification_condition=Disqualification_condition.unknown() ,
                        number_of_rounds=0 ,
                        props=props ,
                        region=Regions.unknown() ,
                        zone=Disqualification_zones.unknown()
                    ) )

                tournament.props = props_t
                tournament.division = division_stage
                tournament.save()

                pbar.update()


def check_divisions() :
    query = Tournaments.objects.filter( division_id__isnull=False ).exclude( division__code=unknown )
    pbar = tqdm( total=query.count() )
    with transaction.atomic() :
        for tournament in query :
            for division in Divisions.objects.filter( id=tournament.division.id ):
                division.region=tournament.region
                division.save()
                if division.parent_id is not None:
                    Divisions.objects.filter( id=division.parent_id ).update(region=tournament.region)

            pbar.update()


class Command( BaseCommand ) :
    help = "Тест функций применяемых в миграциях"

    images_files = set()
    cnt = 1

    def handle( self , *args , **options ) :
        logger.debug( self.help )
        # restruct_divisions()
        check_divisions()
