import logging

from django.db.models import SmallIntegerField , CheckConstraint , Q , F

from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldId
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefHierarcyManager, BaseRefHierarcyQuerySet
from lfl_admin.decor.models.menu_type import Menu_type
from lfl_admin.decor.models.menus import MenusQuerySet, MenusManager, Menus

logger = logging.getLogger(__name__)


class Bottom_menuQuerySet(MenusQuerySet):
    pass


class Bottom_menuManager(MenusManager):

    @classmethod
    def getRecord(cls, record ) :
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
        return Bottom_menuQuerySet(self.model, using=self._db)


class Bottom_menu(Menus, Model_withOldId):

    objects = Bottom_menuManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Нижнее меню Меню'

