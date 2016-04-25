# -*- coding: utf-8 -*-
'''
Module for handling GeoDNS record manipulation.

Author: Total Server Solutions

:configuration: This module is not usable until the following are specified
    either in a pillar or in the minion's config file::

    geodns.datadir = '/var/dns'
    
'''

from __future__ import absolute_import
import os
import json

def _get_zone(name):
    datadir = __pillar__['geodns.datadir']
    zone_file = get_full_path(name)
    if os.path.exists(zone_file):
        with open(zone_file, 'r') as content_file:
            content = content_file.read()
            content = json.loads(content)
        return {zone_file: content}
    return {'Error': 'Could not find zone file {0}'.format(zone_file)}

def get_full_path(name):
    datadir = __pillar__['geodns.datadir']
    if name.startswith(datadir) and name.endswith('.json'):
        zone_file = name
    else:
        zone_file = '{0}/{1}{2}'.format(datadir, name, '.json')
    return zone_file

def get_zone(name):
    zone = _get_zone(name)
    return zone 

def get_record(zone, name):
    zone_file = get_full_path(zone)
    zone_data = _get_zone(zone)
    if name in zone_data[zone_file]['data']:
        return {name: zone_data[zone_file]['data'][name]}
    return {'Error': 'Could not locate name "{0}" in zone "{1}"'.format(name, zone)}

def _save_zone(zone):
    zone_file = zone.keys()[0]
    f = open(zone_file, 'w')
    json_data = json.dumps(zone[zone_file], indent=4, sort_keys=True)
    if json_data:
        f.write(json_data)
        f.close()
        return get_zone(zone_file)
    return {'Error': 'Could not save zone {0}'.format(zone_file)}

# value should be like [ ["192.168.0.1", 100], ["192.168.10.1", 50] ] for simple a record
# only a records allowed for now
def add_record(zone, name, value, type="a"):
    zone_name = get_full_path(zone)
    zone = get_zone(zone_name)
    if name in zone[zone_name]['data']:
        return {'Error': 'Record {0} already exists'.format(name)}
    zone[zone_name]['data'][name] = {"a": value}
    return _save_zone(zone)

# TODO: this just replaces existing zone with data currently without question
def add_zone(name, data={}):
    datadir = __pillar__['geodns.datadir']
    nameservers = __pillar__['geodns.nameservers']
    default_data = {
        "": {
            "ns": nameservers
        },
        "data": {}
    }
    zone_file = get_full_path(name)
    if not data:
        data = default_data
    zone_data = {zone_file: data}
    return _save_zone(zone_data) 

# I believe with geodns, there is only one key in a record for the record type
def get_type(record):
    return record.keys()[0]
        
def update_record(zone, name, value, type=None):
    zone_name = get_full_path(zone)
    zone_data = get_zone(zone_name)
    if name in zone_data[zone_name]['data']:
        if not type:
            type = get_type(record)
        zone_data[zone_name]['data'][name] = {type: value}
    return _save_zone(zone_data)

def delete_record(zone, name):
    zone_name = get_full_path(zone)
    zone_data = get_zone(zone_name)
    if name in zone_data[zone_name]['data']:
        zone_data[zone_name]['data'].pop(name)
    return _save_zone(zone_data)     

