import logging

from bitfield import BitField
from django.db.models import SmallIntegerField
from isc_common.auth.models.user import User
from isc_common.common import unknown, unknown_name
from isc_common.fields.code_field import CodeField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldId

from lfl_admin.competitions.models.leagues import Leagues
from lfl_admin.decor.models.menu_type import Menu_type
from lfl_admin.decor.models.menus import MenusManager, MenusQuerySet, Menus
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger(__name__)


class Menu_itemsQuerySet(MenusQuerySet):
    pass


class Menu_itemsManager(MenusManager):

    @classmethod
    def props(cls):
        return BitField(flags=(
            ('active', 'active'),
            ('target', 'target'),
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
    return Menu_itemsQuerySet(self.model, using=self._db)


class Menu_items(Menus, Model_withOldId):

    props = Menu_itemsManager.props()

    objects = Menu_itemsManager()

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

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Главное меню'
