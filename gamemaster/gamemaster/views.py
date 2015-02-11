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
    characters = {}
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
        characters[c.id] = c
    
    #then we calculate their relationships
    for char in characters:
        log.info(characters[char])
        characters[char].fill_social_vector(characters)
        log.info(characters[char].social_vector)
        characters[char].update_booleans(characters)
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
    dead_characters = []
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
                    if rule.matches(characters[char]):  
                        happened = {'year':3456+i, 'season': season, 'character': characters[char], 'character_img': characters[char].picture, 'name': characters[char].name, 'location': characters[char].location.name, 'action_narrated': rule.do_action(characters[char], characters)}
                        happenings.append(happened)
                        characters[char].update_booleans(characters)
                        characters[char].update_health()
                        if rule.action in ['die', 'suicide']:
                            if characters[char] not in dead_characters:
                                dead_characters.append(characters[char])
                        acted = True
                        break
                if not acted:
                    characters[char].update_booleans(characters)
                    characters[char].update_health()
            #updating deaths

            for char in dead_characters:
                char.location.inhabitants.remove(char)
                char.location.ocupation -= 1
                del characters[char.id]
                for c in characters:
                    characters[c].fill_social_vector(characters)
            dead_characters = []
            log.info("__________________END OF SEASON______________")
        log.info("_______________END OF YEAR_________________")
        for c in characters:
            characters[c].age +=1
    return {'happenings': happenings, 'characters': characters, 'error' : error_msg }