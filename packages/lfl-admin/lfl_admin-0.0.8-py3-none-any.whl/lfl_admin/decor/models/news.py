import logging

from bitfield import BitField
from django.db.models import DateTimeField, SmallIntegerField, BigIntegerField
from isc_common.auth.models.user import User
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditManager, AuditQuerySet, Model_withOldId, AuditModel
from lfl_admin.competitions.models.calendar import Calendar
from lfl_admin.competitions.models.leagues import Leagues
from lfl_admin.competitions.models.tournaments import Tournaments
from lfl_admin.decor.models.news_icon_type import News_icon_type
from lfl_admin.decor.models.news_type import News_type
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger(__name__)


class NewsQuerySet(AuditQuerySet):
    pass


class NewsManager(AuditManager):

    @classmethod
    def props(cls):
        return BitField(flags=(
            ('active', 'active'),  # 0
            ('disable_editor', 'disable_editor'),  # 1
            ('fixed_position', 'fixed_position'),  # 2
            ('in_bottom', 'in_bottom'),  # 3
            ('in_middle', 'in_middle'),  # 4
            ('in_top', 'in_top'),  # 5
        ), default=1, db_index=True)

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return NewsQuerySet(self.model, using=self._db)


class News(AuditModel, Model_withOldId):
    admin = ForeignKeyProtect(User, related_name='News_admin')
    attache_dir = CodeField()
    created = ForeignKeyProtect(User, related_name='News_created')
    date = DateTimeField(blank=True, null=True)
    en = ForeignKeyProtect("self", blank=True, null=True)
    icon = ForeignKeyProtect(News_icon_type, blank=True, null=True)
    league = ForeignKeyProtect(Leagues)
    match = ForeignKeyProtect(Calendar)
    old_image_big_id = BigIntegerField(db_index=True, null=True, blank=True)
    old_image_small_id = BigIntegerField(db_index=True, null=True, blank=True)
    old_tour = CodeField(null=True, blank=True)
    position = SmallIntegerField()
    props = NewsManager.props()
    region = ForeignKeyProtect(Regions)
    tournament = ForeignKeyProtect(Tournaments)
    type = ForeignKeyProtect(News_type)

    objects = NewsManager()

    @classmethod
    def unknown(cls):
        res, _ = cls.objects.get_or_create(
            admin=User.unknown(),
            created=User.unknown(),
            league=Leagues.unknown(),
            match=Calendar.unknown(),
            position=0,
            icon=News_icon_type.unknown(),
            region=Regions.unknown(),
            tournament=Tournaments.unknown(),
            type=News_type.unknown(),
        )
        return res

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Новости, встраиваемые блоки, видео'
