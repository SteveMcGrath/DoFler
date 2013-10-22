from hashlib import md5

def md5hash(*items):
    '''md5hash list, of, items
    A simple convenience function to return a hex md5hash of all of the
    items given.

    :param *items: list of items to hash. 
    :type *items: list
    :return: str 
    '''
    m = md5()
    for item in items:
        m.update(str(item))
    return m.hexdigest()