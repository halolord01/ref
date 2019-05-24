# converts dictionieris into dot access format
import numpy as np
import copy
class DotDict(dict):
    """
    a dictionary that supports dot notation 
    as well as dictionary access notation 
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value

# this copys a standard data definition, dicitonary, and returns a dotdict
# this prevents the pythonic pass by reference messing up data definitions
# and DotDict not liking copy.copy(DotDictItem) fully 
def copy_to_dot(info):
    ret = copy.deepcopy(info)
    return DotDict(ret)

depth_of_list = lambda L: isinstance(L, list) and max(map(depth_of_list, L))+1

# feed a list to print lengths or keys
def treeify(lst, space=0):
  if type(lst) in (list, tuple, np.ndarray):
    # print '{l:{space}}'.format(l=len(lst), space=space)
    # space += 2
    # print '{l:{space}}'.format(l= len(lst), space = space)
    print ' '*space + '{}'.format(len(lst))

    for i in range(len(lst)):
      treeify(lst[i], space=space + 2)
  elif type(lst) is dict:
    for k in lst.keys():
      print ' '* space + '{}'.format(k)
      treeify(lst[k], space = space+2)
  # else:
    # print ' '*space + '{}'.format(type(lst))

# updates the base dict with vales from the new dict
# will add missing keys, but will not override old data 
#    (unless the else case is un-commented)
def dict_meld(base, new):
    for k,v in new.iteritems():
        if k not in base.keys():
            base[k] = v
        elif type(v) is dict:
            base[k] =  upper(base[k], v)
        else:
            # this will override old data with new data
            # skip this to always keep the old data
            # base[k] = v
            pass
            
    return base
