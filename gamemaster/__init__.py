from pyramid.config import Configurator

from pyramid.view import view_config
import logging

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('home2', '/test/{foo}')
    config.add_route('home3', '/othertest/{foo2}')
    config.scan()
    return config.make_wsgi_app()
