import logging

from isc_common.common import unknown, unknown_name
from isc_common.models.base_ref import BaseRef, BaseRefManager, BaseRefQuerySet

logger = logging.getLogger(__name__)


class Menu_typeQuerySet(BaseRefQuerySet):
    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Menu_typeManager(BaseRefManager):

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Menu_typeQuerySet(self.model, using=self._db)


class Menu_type(BaseRef):
    objects = Menu_typeManager()

    @classmethod
    def unknown(cls):
        res, _ = cls.objects.get_or_create(
            code = unknown,
            defaults=dict(name=unknown_name)
        )
        return res

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Типы банеров'
