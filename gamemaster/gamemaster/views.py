from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

from character import Character
import locations as l
import generation as g
import random as r
import json
import logging

log = logging.getLogger(__name__)

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'gamemaster'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_gamemaster_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='generate', renderer='templates/foo.mako')
@view_config(route_name='generate_with_number', renderer='templates/foo.mako')
def generate(request):
    locations = l.generate()
    log.info(locations)
    characters = []

    #we generate all characters first
    for char_ind in range(int(request.matchdict['number_of_characters'])):
        c = Character()
        full_locs = []
        error_msg = ''
        possible_locations = [i for i in range(len(locations)) if not locations[i].is_full() and locations[i].can_work(c)]
        log.info(possible_locations)
        log.info(len(possible_locations))
        if len(possible_locations) == 0:
            error_msg = "Not enough available locations. " + str(char_ind) + " characters weren't generated"
            break
        else:
            loc = locations[possible_locations[r.randint(0, len(possible_locations)-1)]]
            c.set_location(loc)
            loc.increase_ocupation()
        characters.append(c)
    
    #then we calculate their relationships
    for char1 in characters:
        log.info(char1.name)
        for char2 in characters:
            log.info(char1 == char2)


    return {'foo' : characters, 'bar': locations, 'error' : error_msg }