import logging

from bitfield import BitField
from django.db.models import DateTimeField, BigIntegerField

from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet, Model_withOldId
from lfl_admin.competitions.models.tournaments import Tournaments

logger = logging.getLogger(__name__)


class News_start_block_tournamentQuerySet(AuditQuerySet):
    pass


class News_start_block_tournamentManager(AuditManager):

    @classmethod
    def props(cls):
        return BitField(flags=(
            ('active', 'active'),  # 1
            ('disable_editor', 'disable_editor'),  # 1
            ('in_middle', 'in_middle'),  # 1
            ('in_top', 'in_top'),  # 1
        ), default=1, db_index=True)

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return News_start_block_tournamentQuerySet(self.model, using=self._db)


class News_start_block_tournament(AuditModel, Model_withOldId):
    admin = ForeignKeyProtect(User, related_name='News_start_block_tournament_admin')
    created = ForeignKeyProtect(User, related_name='News_start_block_tournament_created')
    date = DateTimeField(blank=True, null=True)
    old_image_big_id = BigIntegerField(db_index=True, null=True, blank=True)
    old_image_small_id = BigIntegerField(db_index=True, null=True, blank=True)
    props = News_start_block_tournamentManager.props()
    tournament = ForeignKeyProtect(Tournaments)

    objects = News_start_block_tournamentManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Новости, встраиваемые блоки, видео'
