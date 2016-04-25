'''
GeoDNS state module for use with GeoDNS salt module.
Author: Total Server Solutions

Todo: document these a little nicer if we want to open-source these

'''
def __virtual__():
    return 'geodns'

# compare record values even if order is different
# convert lists of lists to tuples since they are hashable
def _values_equal(list1, list2):
    set1 = set(map(tuple, list1))
    set2 = set(map(tuple, list2))
    return set1 == set2

def record_present(zone, name, value, type=None):
    ret = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': 'Record "{0}" already exists.'.format(name)
    }
    record = __salt__['geodns.get_record'](zone=zone,
                                            name=name)
    if 'Error' not in record:
        if type is None:
            type = __salt__['geodns.get_type'](record[name])
        for file_name, content in record.iteritems():
            current_value = content[type]
            if not _values_equal(current_value, value):
                __salt__['geodns.update_record'](zone=zone,
                                                name=name,
                                                value=value,
                                                type=type)
            ret['comment'] = 'Record "{0}" has been updated.'.format(name)
            ret['changes']['Ips'] = 'Updated.'
    else:
        if type is None:
            type = 'a'
        record = __salt__['geodns.add_record'](zone=zone,
                                                name=name,
                                                value=value,
                                                type=type)

        ret['comment'] = 'Record "{0}" has been added.'.format(name)
        ret['changes']['Record'] = 'Created.'
    return ret

def zone_present(name, zone_data={}):
    modified = False
    ret = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': 'Zone "{0}" already exists.'.format(name)
    }
    zone = __salt__['geodns.get_zone'](name)
    key = __salt__['geodns.get_full_path'](name)
    # Zone does not exist yet
    if 'Error' in zone:
        zone = __salt__['geodns.add_zone'](name, zone_data)
        ret['comment'] = 'Zone "{0}" has been created.'.format(name)
        ret['changes']['Zone'] = 'Created.'
    else:
        if zone_data and zone_data != zone[key]:
            zone = __salt__['geodns.add_zone'](name, zone_data)
            ret['comment'] = 'Zone "{0}" has been updated.'.format(name)
            ret['changes']['Zone'] = 'Updated.'
    return ret

