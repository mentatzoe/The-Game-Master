from pyramid.view import view_config
import logging
import json

log = logging.getLogger(__name__)
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'GameMaster'}

@view_config(route_name='home2', renderer='templates/mytemplate2.pt')
def my_view2(request):
    log.info('asdf')
    log.info(request.matchdict)
    return {'bar': request.matchdict['foo']}

@view_config(route_name='home3', renderer='templates/foo.pt')
def idk(request):
    log.info("Something else")
    log.info(request.matchdict)
    yet_another_test = int(request.matchdict['foo2']) * 3
    return {'foo': json.dumps({'foo': yet_another_test})}