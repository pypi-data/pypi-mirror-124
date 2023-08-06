import logging

from django.db.models import DateTimeField, TextField
from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModelQuerySet, AuditModelManager, AuditModel, Model_withOldId

from lfl_admin.decor.models.news import News
from lfl_admin.decor.models.news_action_types import News_action_types

logger = logging.getLogger(__name__)


class News_actionsQuerySet(AuditModelQuerySet):
    pass


class News_actionsManager(AuditModelManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return News_actionsQuerySet(self.model, using=self._db)


class News_actions(AuditModel, Model_withOldId):
    dt = DateTimeField()
    from_data = TextField(blank=True, null=True)
    from_tag = TextField(blank=True, null=True)
    new = ForeignKeyProtect(News)
    to_data = TextField(blank=True, null=True)
    to_tag = TextField(blank=True, null=True)
    type = ForeignKeyProtect(News_action_types)
    user = ForeignKeyProtect(User)

    objects = News_actionsManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Действия'
