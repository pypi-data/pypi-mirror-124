from django.utils.translation import ugettext_lazy as _
from bitfield import BitField

import logging

from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditModelManager, AuditModelQuerySet, Model_withOldId

from lfl_admin.competitions.models.leagues import Leagues
from lfl_admin.decor.models.menu_items import Menu_items
from lfl_admin.decor.models.menu_type import Menu_type
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger(__name__)


class Menu_item_leaguesQuerySet(AuditModelQuerySet):
    pass


class Menu_item_leaguesManager(AuditModelManager):

    @classmethod
    def props(cls):
        return BitField(flags=(
        ), default=0, db_index=True)

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Menu_item_leaguesQuerySet(self.model, using=self._db)


class Menu_item_leagues(AuditModel, Model_withOldId):
    league = ForeignKeyProtect(Leagues)
    menu_item = ForeignKeyProtect(Menu_items)
    region = ForeignKeyProtect(Regions)

    objects = Menu_item_leaguesManager()

    @classmethod
    def unknown(cls):
        res, _ = cls.objects.get_or_create(
            menu_type=Menu_type.unknown(),
            league=Leagues.unknown(),
            region=Regions.unknown(),
        )
        return res

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
