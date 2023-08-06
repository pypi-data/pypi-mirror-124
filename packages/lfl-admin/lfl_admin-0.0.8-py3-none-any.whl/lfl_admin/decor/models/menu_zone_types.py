from django.utils.translation import ugettext_lazy as _
from bitfield import BitField

import logging

from isc_common.common import unknown, unknown_name
from isc_common.models.base_ref import BaseRef, BaseRefManager, BaseRefQuerySet

logger = logging.getLogger(__name__)


class Menu_zone_typesQuerySet(BaseRefQuerySet):
    pass


class Menu_zone_typesManager(BaseRefManager):

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
        return Menu_zone_typesQuerySet(self.model, using=self._db)


class Menu_zone_types(BaseRef):
    objects = Menu_zone_typesManager()

    @classmethod
    def unknown(cls):
        res, _ = cls.objects.get_or_create(
            code=unknown,
            defaults=dict(name=unknown_name)
        )
        return res

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Типы зон'
