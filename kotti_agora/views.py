import colander
import deform

from plone.batching import Batch

from kotti import DBSession
from kotti.resources import get_root
from kotti.security import has_permission
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.views.util import template_api

from kotti_agora import agora_settings
from kotti_agora.models import Idea
from kotti_agora.models import Forum

from pyramid.renderers import get_renderer
from pyramid.view import view_config
from pyramid.view import view_defaults

import logging
logger = logging.getLogger("%s: " % str(__name__))

class ForumSchema(colander.MappingSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=u'Title',
        )
        
class IdeaSchema(colander.MappingSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=u'Title',
        )
    body = colander.SchemaNode(
        colander.String(),
        title=u'Idea',
        widget=deform.widget.TextAreaWidget(rows=25, cols=60),
        )

class ForumEditForm(EditFormView):
    schema_factory = ForumSchema
    
class ForumAddForm(AddFormView):
    schema_factory = ForumSchema
    add = Forum
    item_type = u'Forum'
        
class IdeaEditForm(EditFormView):
    schema_factory = IdeaSchema
    
class IdeaAddForm(AddFormView):
    schema_factory = IdeaSchema
    add = Idea
    item_type = u"Idea"


@view_defaults(name='view', permission='view')
class Views:

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def agora_front_page_view(self):
        """"""
        logger.info("agora_front_page_view: ")
        return {}
    
    @view_config(context=Forum,
                 renderer='kotti_agora:templates/forum_view.pt')
    def view_forum(self):
        logger.info("views: view_forum: ")
        settings = agora_settings()
        macros = get_renderer('templates/macros.pt').implementation()
        session = DBSession()
        query = session.query(Idea).order_by(Idea.date.desc())
        items = query.all()
        items = [item for item in items if has_permission('view', item, self.request)]
        page = self.request.params.get('page', 1)
        if settings['use_batching']:
            items = Batch.fromPagenumber(items,
                          pagesize=settings['pagesize'],
                          pagenumber=int(page))
        return {
            'api': template_api(self.context, self.request),
            'macros': macros,
            'items': items,
            'settings': settings,
            }

    @view_config(context=Idea,
                 renderer='kotti_agora:templates/idea_view.pt')
    def view_idea(self):
        return {}
        
def includeme_edit(config):

    config.add_view(
        ForumAddForm,
        name='add_forum',
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )
        
    config.add_view(
        ForumEditForm,
        context=Forum,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )
    
    config.add_view(
        IdeaAddForm,
        name='add_idea',
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )
        
    config.add_view(
        IdeaEditForm,
        context=Idea,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )
        
def populate():
    site = get_root()
    site.default_view = 'agora_front_page_view'

def includeme(config):
    logger.info("includeme: ")
    config.add_view(
        name='agora_front_page_view',
        renderer='kotti_agora:templates/agora_front_page.pt',
    )
    settings = config.get_settings()
    if 'kotti_agora.asset_overrides' in settings:
        for override in [a.strip()
                         for a in settings['kotti_agora.asset_overrides'].split()
                         if a.strip()]:
            config.override_asset(to_override='kotti_agora', override_with=override)
    includeme_edit(config)
    config.add_static_view('static-kotti_agora', 'kotti_agora:static')
    config.scan(__name__)

if __name__ == '__main__':
    logger.info("views: ")
