"""
Main entry point
"""
from pyramid.config import Configurator

from broadlink_rest import views


def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # routes
    config.add_route('device_info', '/device/info/{mac}/{ip}')
    config.add_route('device_cmd_sp2_power', '/device/command/sp2/power/{mac}/{ip}/set/{power}')
    config.add_route('device_cmd_sp2_state', '/device/command/sp2/state/{mac}/{ip}')
    
    config.add_route('device_cmd_a1_state', '/device/command/a1/state/{mac}/{ip}/raw/{raw}')
    
    # Cornice
    config.include("cornice")
    config.scan("broadlink_rest.views")
    
    return config.make_wsgi_app()

