import datetime

from kotti.resources import Content
from kotti.resources import TypeInfo
from kotti.resources import get_root

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Text,
    ForeignKey,
    UniqueConstraint,
    Index,
    types,
)

import logging
logger = logging.getLogger("%s: " % str(__name__))

class UTCDateTime(types.TypeDecorator):
    impl = types.DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            return value.astimezone(tzutc())

    def process_result_value(self, value, engine):
        if value is not None:
            return datetime.datetime(value.year, value.month, value.day,
                    value.hour, value.minute, value.second, value.microsecond,
                    tzinfo=tzutc())

class ForumTypeInfo(TypeInfo):

    def addable(self, context, request):
        """add once, and only to the root"""
        addable = context == get_root()
        child_type_already_added = self in [
                c.type_info for c in context.children]
        return addable and not child_type_already_added

class Forum(Content):
    """A forum is added to the site root. 
       Ideas are added to the forum."""
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)
    
    type_info = ForumTypeInfo(
        name=u'Forum',
        title=u'Forum',
        add_view=u'add_forum',
        addable_to=[u'Document'],
        )


class Idea(Content):
    """Ideas are added to the forum."""
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)
    body = Column(Text())
    date = Column('date', UTCDateTime())

    type_info = Content.type_info.copy(
        name=u'Idea',
        title=u'Idea',
        add_view=u'add_idea',
        addable_to=[u'Forum'],
        )

    def __init__(self, body, date=None, **kwargs):
        super(Idea, self).__init__(**kwargs)
        self.body = body
        self.date = date

