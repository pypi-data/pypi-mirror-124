from django.utils.translation import ugettext_lazy as _

import logging

from isc_common.common import unknown , unknown_name
from isc_common.models.base_ref import BaseRefQuerySet , BaseRefManager , BaseRef

logger = logging.getLogger( __name__ )


class Rating_ruleQuerySet( BaseRefQuerySet ) :
    pass


class Rating_ruleManager( BaseRefManager ) :

    @classmethod
    def getRecord(cls, record )  :
        res = {
            'id' : record.id ,
            'code' : record.code ,
            'name' : record.name ,
            'description' : record.description ,
            'editing' : record.editing ,
            'deliting' : record.deliting ,
        }
        return res

    def get_queryset( self ) :
        return Rating_ruleQuerySet( self.model , using=self._db )


class Rating_rule( BaseRef ) :
    objects = Rating_ruleManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.update_or_create(
            code=unknown ,
            defaults=dict( name=unknown_name )
        )
        return res

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Правила учета очков при их равенстве'
