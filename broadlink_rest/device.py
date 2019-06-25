

import broadlink

"""
Serialize device object to dict type
"""
def to_dict(device):

    device_d = dict(
            type = device.type,
            host = device.host,
            ip = device.host[0],
            port = device.host[1],
            mac = ':'.join(format(x, '02x') for x in bytearray(device.mac)),
            mac_raw = ''.join(format(x, '02x') for x in bytearray(device.mac)),
            timeout = device.timeout,
            count = device.count,
            iv = ''.join(format(x, '02x') for x in bytearray(device.iv)),
            id = ''.join(format(x, '02x') for x in bytearray(device.id))
            )

    return device_d

"""
Convert list of device objects to 
"""
def to_list(devices):

    device_list = [ ]

    for device_obj in devices:
        device_dict = to_dict(device_obj)
        device_list.append(device_dict)

    return device_list

"""
Get all devices as a list of serialized to dict device objects
"""
def list_all(timeout=5):

    devices = to_list(broadlink.discover(timeout))

    return devices

"""
Get device by mac and IP(host)
"""
def get(mac, ip, dev_type = 0):
    
    mac = bytearray.fromhex(mac)   

    dev = broadlink.gendevice(dev_type, (ip, 80), mac)
    
    dev.auth()
    
    return dev
    
    
    

