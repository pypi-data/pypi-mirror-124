import logging

from isc_common.fields.related import ForeignKeyProtect , ForeignKeyCascade
from isc_common.models.image_types import Image_types
from isc_common.models.images import Images
from isc_common.models.model_images import Model_imagesManager , Model_imagesQuerySet , Model_images
from lfl_admin.competitions.models.leagues import Leagues

logger = logging.getLogger(__name__)


class Leagues_imagesQuerySet(Model_imagesQuerySet):
    pass


class Leagues_imagesManager(Model_imagesManager):

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Leagues_imagesQuerySet(self.model, using=self._db)


class Leagues_images(Model_images):
    image = ForeignKeyProtect(Images)
    main_model = ForeignKeyCascade(Leagues)
    type = ForeignKeyProtect(Image_types)

    objects = Leagues_imagesManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
        unique_together = (('main_model', 'image', 'type', 'deleted_at'),)
