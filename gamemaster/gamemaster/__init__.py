from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

from pyramid.session import SignedCookieSessionFactory


from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = SignedCookieSessionFactory('idontreallyneedthistobesupersecret')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('generate', '/generate')
    config.add_route('generate_with_number', '/generate/{num_characters}')
    config.add_route('generate_story', '/story')
    config.add_static_view(name='/images/', path=config.registry.settings['img_dir'])
    config.set_session_factory(my_session_factory)
    config.scan()
    
    return config.make_wsgi_app()
