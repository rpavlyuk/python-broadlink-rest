""" Cornice services.
"""
from cornice import Service
from pyramid.view import view_config
from pyramid.response import Response
from broadlink_rest import device
import json

import logging
log = logging.getLogger(__name__)



devices = Service(name='devices', path='/devices', description="BroadLink Devices")

def make_response(response_data):
    
    control = dict()  # store service information in 'control' section  
    content = json.dumps(dict(data = response_data, control = control))
    
    response = Response(content)
    response.content_type = 'application/json'
    
    return response


@devices.get()
def get_info(request):

    devices = device.list_all()

    return devices


@view_config(route_name='device_info', request_method='GET')
def get_device(request):
    
    d = device.get(request.matchdict['mac'], request.matchdict['ip'])
    
    return make_response(device.to_dict(d))


@view_config(route_name='device_cmd_sp2_power', request_method='GET')
def device_command_sp2_power(request):
    
    d = device.get(request.matchdict['mac'], request.matchdict['ip'], 0x2711 ) # force SP2 device type
    log.debug("Setting power state: " + str(bool(request.matchdict['power'] == '1')))   
    d.set_power(bool(request.matchdict['power'] == '1'))
    
    return make_response(
            dict(device = device.to_dict(d), 
            state = dict(
                power = 1 if d.check_power() else 0, 
                energy = d.get_energy() if "get_energy" in dir(d) else 0
                )
             )
        )
   
@view_config(route_name='device_cmd_sp2_state', request_method='GET')
def device_command_sp2_state(request):
    
    d = device.get(request.matchdict['mac'], request.matchdict['ip'], 0x2711 ) # force SP2 device type
    
    return make_response(
            dict(device = device.to_dict(d), 
            state = dict(
                power = 1 if d.check_power() else 0, 
                energy = d.get_energy() if "get_energy" in dir(d) else 0
                )
             )
        )
    

@view_config(route_name='device_cmd_a1_state', request_method='GET')
def device_command_a1_state(request):
    
    d = device.get(request.matchdict['mac'], request.matchdict['ip'], 0x2714 ) # force A1 device type
    
    if request.matchdict['raw'] == '1':
        state = d.check_sensors_raw()
    else:
        state = d.check_sensors()
    
    return make_response(
            dict(device = device.to_dict(d), 
            state = state
             )
        )   
    
    
