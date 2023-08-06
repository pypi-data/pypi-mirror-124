import logging

from django.db.models import SmallIntegerField, CheckConstraint, Q, F
from isc_common.common import unknown, unknown_name

from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldId
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefHierarcyManager, BaseRefHierarcyQuerySet
from lfl_admin.decor.models.menu_type import Menu_type

logger = logging.getLogger(__name__)


class MenusQuerySet(BaseRefHierarcyQuerySet):
    pass


class MenusManager(BaseRefHierarcyManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'parent': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return MenusQuerySet(self.model, using=self._db)


class Menus(BaseRefHierarcy):
    position = SmallIntegerField(null=True, blank=True)
    menu_type = ForeignKeyProtect(Menu_type)
    objects = MenusManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def unknown(cls):
        res, _ = cls.objects.get_or_create(
            code=unknown,
            defaults=dict(
                menu_type=Menu_type.unknown(),
                name=unknown_name
            )
        )
        return res

    class Meta:
        verbose_name = 'Меню'
        constraints = [
            CheckConstraint(check=~Q(id=F('parent_id')), name=f'c_Menus'),
        ]
