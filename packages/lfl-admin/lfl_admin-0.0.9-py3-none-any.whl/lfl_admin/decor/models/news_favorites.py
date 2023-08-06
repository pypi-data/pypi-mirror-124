import logging

from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet, Model_withOldId
from lfl_admin.decor.models.news import News

logger = logging.getLogger(__name__)


class News_favoritesQuerySet(AuditQuerySet):
    pass


class News_favoritesManager(AuditManager):

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return News_favoritesQuerySet(self.model, using=self._db)


class News_favorites(AuditModel, Model_withOldId):
    admin = ForeignKeyProtect(User)
    new = ForeignKeyProtect(News)
    objects = News_favoritesManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = ''
