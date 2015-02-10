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
        if characters[char.social_vector.index(min(char.social_vector))].location == char.location:
            log.info("Friend is" +characters[char.social_vector.index(min(char.social_vector))].name)
            char.friend_in_location_atr = True
        if characters[char.social_vector.index(max(char.social_vector))].location == char.location:
            log.info("Enemy is "+characters[char.social_vector.index(max(char.social_vector))].name)
            char.enemy_in_location_atr = True
        if char.profession in char.location.actions['work']:
            char.can_work_atr = True
        characters_in_loc = [c for c in characters if c.location == char.location and c.profession == 'doctor']
        if len(characters_in_loc) > 0:
            char.doctor_available_atr = True
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
                        happenings.append(season + " of Year " + str(i) + ": " + rule.do_action(char, characters) + " " + str(char.happiness))
                        char.update_booleans(characters)
                        char.update_health()
                        acted = True
                        break
                if not acted:
                    happenings.append(season + " of Year " + str(i) + ": " + char.name + " didn't do anything relevant.")
                    char.update_booleans(characters)
                    char.update_health()
        happenings.append("________________________________")
    return {'foo' : ['a', 'b'], 'bar': happenings, 'error' : error_msg }