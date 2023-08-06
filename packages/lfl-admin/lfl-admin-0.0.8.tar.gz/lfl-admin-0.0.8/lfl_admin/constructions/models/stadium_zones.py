import logging

from django.db.models import BigIntegerField, UniqueConstraint, Q
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from lfl_admin.competitions.models.leagues import Leagues
from lfl_admin.constructions.models.stadiums import Stadiums

logger = logging.getLogger(__name__)


class Stadium_zonesQuerySet(AuditQuerySet):
    pass


class Stadium_zonesManager(AuditManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'deliting': record.deliting,
            'editing': record.editing,
            'id': record.id,
            'league__name': record.league.name,
            'league_id': record.league.id,
        }
        return res

    def get_queryset(self):
        return Stadium_zonesQuerySet(self.model, using=self._db)


class Stadium_zones(AuditModel):
    stadium = ForeignKeyProtect(Stadiums)
    old_stadium_id = BigIntegerField(db_index=True)
    league = ForeignKeyProtect(Leagues)
    old_league_id = BigIntegerField(db_index=True)

    objects = Stadium_zonesManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Сортировка стадионов'
        constraints = [
            UniqueConstraint(fields=['league', 'stadium'], condition=Q(old_league_id=None) & Q(old_stadium_id=None), name='Stadium_zones_unique_constraint_0'),
            UniqueConstraint(fields=['league', 'old_stadium_id', 'stadium'], condition=Q(old_league_id=None), name='Stadium_zones_unique_constraint_1'),
            UniqueConstraint(fields=['league', 'old_league_id', 'stadium'], condition=Q(old_stadium_id=None), name='Stadium_zones_unique_constraint_2'),
            UniqueConstraint(fields=['league', 'old_league_id', 'old_stadium_id', 'stadium'], name='Stadium_zones_unique_constraint_3'),
        ]

