import logging

from isc_common.fields.code_field import CodeStrictField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager
from isc_common.models.links import Model_linksQuerySet, Links
from lfl_admin.decor.models.news import News
from lfl_admin.decor.models.news_start_block_tournament import News_start_block_tournament

logger = logging.getLogger(__name__)


class News_start_block_tournament_linksQuerySet(Model_linksQuerySet):
    pass


class News_start_block_tournament_linksManager(AuditManager):

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return News_start_block_tournament_linksQuerySet(self.model, using=self._db)


class News_start_block_tournament_links(AuditModel):
    code = CodeStrictField()
    link = ForeignKeyProtect(Links)
    block = ForeignKeyProtect(News_start_block_tournament)

    objects = News_start_block_tournament_linksManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
        unique_together = (('link', 'block', 'code'),)
