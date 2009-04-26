
import os
import xml.etree.ElementTree
import xml.parsers.expat
import __builtin__
from views import ProfileView
from views import StringView

class aMSNProfile(object):
    """ aMSNProfile : a Class to represent an aMSN profile
    This class will contain all settings relative to a profile
    and will store the protocol and GUI objects
    """
    def __init__(self, profileview, core, profiles_dir):
        self.view = profileview
        #TODO

class aMSNProfileManager(object):
    """ aMSNProfileManager : The profile manager that takes care of storing
    and retreiving all the profiles for our users.
    """
    def __init__(self, options):
        if os.name == "posix":
            self._profiles_dir = os.path.join(os.environ['HOME'], ".amsn2")
        elif os.name == "nt":
            self._profiles_dir = os.path.join(os.environ['USERPROFILE'], "amsn2")
        else:
            self._profiles_dir = os.path.join(os.curdir, "amsn2_profiles")

        try :
            os.makedirs(self._profiles_dir, 0777)
        except :
            pass

        self.profileviews = []
        self.reload()

        if options.account is not None:
            pv = [p for p in self.profileviews if p.email == options.account]
            if pv:
                self.profileviews.remove(pv[0])
            else:
                pv = ProfileView()
                pv.email = options.account
                pv.password = options.password
            self.profileviews.insert(0, pv)

    def reload(self):
        self.profileviews = []
        #TODO
        pass

    def getAllProfileViews(self):
        #TODO
        pass

    def getAvailableProfileViews(self):
        #TODO
        return self.profileviews
        pass

    def signingToProfile(self, profileview):
        #TODO
        pass

    def loadProfile(self, profileview, core):
        #TODO
        return aMSNProfile(profileview, core)

    def unloadProfile(self, amsnprofile):
        #TODO: unlock the profile
        pass


def elementToDict(element):
    """ Converts an XML Element into a proper profile dictionary """
    def dictToTuple(name, dict):
        """ Converts a dictionary returned by expat XML parser into a proper tuple and adds it to a list ready for dict() """
        key = dict['name']
        type = dict['type']
        if type == "bool":
            value = int(dict['value'])
        else:
            value = dict['value']

        config_pair = (key,eval(type)(value))

        config_pair_list.append(config_pair)

    config_pair_list = []

    for entry in element :
        entry_str = xml.etree.ElementTree.tostring(entry)

        parser=xml.parsers.expat.ParserCreate()
        parser.StartElementHandler = dictToTuple
        parser.Parse(entry_str, 1)
        del parser

    config_dict = dict(config_pair_list)

    return config_dict

def dictToElement(name, dict):
    """ Converts a dictionary into a proper XML Element with tag 'name' """
    keys=[]
    types=[]
    values=[]

    root_element = xml.etree.ElementTree.Element(name)

    for key, value in dict.iteritems() :
        keys.append(key)
        type = str(__builtin__.type(value))[7:-2]
        types.append(type)
        if type == "bool":
            int_value = int(value)
            values.append(str(int_value))
        else:
            values.append(str(value))

    for key, type, value in zip(keys, types, values) :
        element = xml.etree.ElementTree.Element("entry", {"name":key, "type":type, "value":value})
        root_element.append(element)

    return root_element
