import logging

from isc_common.fields.code_field import CodeStrictField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager
from isc_common.models.links import Model_linksQuerySet, Links

from lfl_admin.decor.models.menu_items import Menu_items

logger = logging.getLogger(__name__)


class Menu_items_linksQuerySet(Model_linksQuerySet):
    pass


class Menu_items_linksManager(AuditManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Menu_items_linksQuerySet(self.model, using=self._db)


class Menu_items_links(AuditModel):
    code = CodeStrictField()
    link = ForeignKeyProtect(Links)
    menu_item = ForeignKeyProtect(Menu_items)

    objects = Menu_items_linksManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
        unique_together = (('link', 'menu_item', 'code'),)
