import logging

from isc_common.fields.code_field import CodeStrictField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager
from isc_common.models.links import Model_linksQuerySet, Links
from lfl_admin.competitions.models.leagues import Leagues

logger = logging.getLogger(__name__)


class Leagues_linksQuerySet(Model_linksQuerySet):
    pass


class Leagues_linksManager(AuditManager):

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Leagues_linksQuerySet(self.model, using=self._db)


class Leagues_links(AuditModel):
    code = CodeStrictField()
    link = ForeignKeyProtect(Links)
    league = ForeignKeyProtect(Leagues)

    objects = Leagues_linksManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
