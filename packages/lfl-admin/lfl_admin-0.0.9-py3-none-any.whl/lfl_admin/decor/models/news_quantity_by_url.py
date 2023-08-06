import logging

from django.db.models import URLField, SmallIntegerField
from isc_common.models.audit import AuditModel, AuditModelQuerySet, AuditModelManager

logger = logging.getLogger(__name__)


class NewsQuantity_ByUrlQuerySet(AuditModelQuerySet):
    pass


class NewsQuantity_ByUrlManager(AuditModelManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return NewsQuantity_ByUrlQuerySet(self.model, using=self._db)


class NewsQuantity_ByUrl(AuditModel):
    url = URLField(max_length=255, unique=True)
    quantity = SmallIntegerField()

    objects = NewsQuantity_ByUrlManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Ограничение на количество новостей'
