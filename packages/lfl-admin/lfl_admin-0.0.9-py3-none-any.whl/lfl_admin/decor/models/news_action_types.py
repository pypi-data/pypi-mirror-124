from django.utils.translation import ugettext_lazy as _
from bitfield import BitField

import logging

from isc_common.models.base_ref import BaseRefManager, BaseRefQuerySet, BaseRef

logger = logging.getLogger(__name__)


class News_action_typesQuerySet(BaseRefQuerySet):
    pass


class News_action_typesManager(BaseRefManager):

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
        return News_action_typesQuerySet(self.model, using=self._db)


class News_action_types(BaseRef):
    objects = News_action_typesManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Типы действий'
