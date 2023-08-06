from django.utils.translation import ugettext_lazy as _
from bitfield import BitField

import logging

from isc_common.fields.related import ForeignKeyCascade, ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditModelManager, AuditModelQuerySet, Model_withOldId

from lfl_admin.competitions.models.disqualification_zones import Disqualification_zones
from lfl_admin.decor.models.menu import Menu
from lfl_admin.decor.models.menu_zone_types import Menu_zone_types
from lfl_admin.decor.models.menus import Menus

logger = logging.getLogger(__name__)


class Menu_zonesQuerySet(AuditModelQuerySet):
    pass


class Menu_zonesManager(AuditModelManager):

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
        return Menu_zonesQuerySet(self.model, using=self._db)


class Menu_zones(AuditModel, Model_withOldId):
    menu = ForeignKeyProtect(Menu)
    zone = ForeignKeyProtect(Disqualification_zones)
    type = ForeignKeyProtect(Menu_zone_types)

    objects = Menu_zonesManager()

    @classmethod
    def unknown(cls):
        res, _ = cls.objects.get_or_create(
            menu=Menu.unknown(),
            zone=Disqualification_zones.unknown(),
            type=Menu_zone_types.unknown(),
        )
        return res

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
