from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

from character import Character
import rules as ru
import locations as l
import generation as g
import random as r
import json
import logging
import pickle

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
    session = request.session
    locations = l.generate()
    characters = []
    char_num = int(request.matchdict['number_of_characters'])
    #we generate all characters first
    for char_ind in range(char_num):
        c = Character()
        c.id = char_ind
        full_locs = []
        error_msg = ''
        possible_locations = [i for i in range(len(locations)) if not locations[i].is_full() and locations[i].can_work(c)]
        if len(possible_locations) == 0: #consider generating a new character
            error_msg = "Not enough available locations. " + str(char_num - char_ind) + " characters weren't generated."
            break
        else:
            loc = locations[possible_locations[r.randint(0, len(possible_locations)-1)]]
            c.set_location(loc)
            loc.inhabitants.append(c)
            loc.increase_ocupation()
        characters.append(c)
    
    #then we calculate their relationships
    for char in characters:
        char.fill_social_vector(characters)
        log.info(char.social_vector)
        char.update_booleans(characters)
        #Calculate can_work, doctor_available, friend/enemy_in_location
    #session['chars'] = characters
    model = MyModel()
    model.name = 'characters' + str(r.random() * 100)
    model.value = str(pickle.dumps(characters))
    db_characters = DBSession.add(model)
    session['chars'] = model.name
    return {'foo' : characters, 'bar': locations, 'error' : error_msg }

@view_config(route_name='generate_story', renderer='templates/foo2.mako')
def generate_story(request):
    session = request.session
    log.info(session)
    happenings = []
    error_msg = ''
    characters_pre = DBSession.query(MyModel).filter(MyModel.name == session['chars']).one()
    characters = pickle.loads(characters_pre.value)
    rules = ru.render_rules()
    acted = False
    for i in range(5):
        for season in ['Summer', 'Fall', 'Winter', 'Spring']:
            for char in characters:
                acted = False
                for rule in rules:
                    if rule.matches(char):
                        if char.sick():
                            log.info(str(i) + season + char.name + " Character is sick")
                        happenings.append(season + " of Year " + str(i) + ": " + rule.do_action(char, characters) + " " + str(char.happiness))
                        char.update_booleans(characters)
                        char.update_health()
                        acted = True
                        log.info("RULE TRIGGERED " + str(rule))
                        break
                if not acted:
                    log.info(char.name + "DIDNT ACT -----")
                    log.info("# rules " + str(len(rules)))
                    log.info(rules[23].matches(char))
                    char.log_booleans()
                    char.update_booleans(characters)
                    char.update_health()
                    log.info("_______________________________")
            happenings.append("________________________________")
        happenings.append("________________________________")
    return {'foo' : ['a', 'b'], 'bar': happenings, 'error' : error_msg }