from .MacInfo import *
from .PortInfo import *

def load_macs(device, ports, arps):
    response = device.send_request('/mac-table', 'GET', 'port_element')

    for item in response['mac_table_entry_element']:
        mac = MacInfo(item)
        if mac.mac in arps.keys():
            mac.setIP(arps[mac.mac])
        # add fake port, not obtained from REST
        if mac.port not in ports.keys():
            item['id'] = mac.port
            item['name'] = "unknown port, added by MacInfo"
            ports[mac.port] = PortInfo(item)
        ports[mac.port].addMac(mac)
    return


def load_ports(device, statuses):
    response = device.send_request('/ports', 'GET', 'port_element')
    ports = {}

    for i in response['port_element']:
        port = PortInfo(i)
        if port.id in statuses:
            port.addStatus(statuses[port.id]['status'])
        ports[port.id] = port
    return ports


def load_status(device):
    response = device.send_request('/system/status/switch', 'GET', 'port_element')
    statuses = {}

    for i in response['blades']:
        for port in i['data_ports']:
            id = str(port['port_id'])
            statuses[id] = {}
            statuses[id]['status'] = port['operStatus']
    return statuses

