import os
import xml.etree.ElementTree
import xml.parsers.expat
import __builtin__
from views import AccountView
from views import StringView

class aMSNAccount(object):
    """ aMSNAccount : a Class to represent an aMSN account
    This class will contain all settings relative to an account
    and will store the protocol and GUI objects
    """
    def __init__(self, accountview, core, account_dir):
        self.view = profileview
        #TODO

class aMSNAccountManager(object):
    """ aMSNAccountManager : The account manager that takes care of storing
    and retreiving all the account.
    """
    def __init__(self, options):
        if os.name == "posix":
            self._accounts_dir = os.path.join(os.environ['HOME'], ".amsn2")
        elif os.name == "nt":
            self._accounts_dir = os.path.join(os.environ['USERPROFILE'], "amsn2")
        else:
            self._accounts_dir = os.path.join(os.curdir, "amsn2_accounts")

        try :
            os.makedirs(self._accounts_dir, 0777)
        except :
            pass

        self.accountviews = []
        self.reload()

        if options.account is not None:
            pv = [p for p in self.accountviews if p.email == options.account]
            if pv:
                self.accountviews.remove(pv[0])
            else:
                pv = AccountView()
                pv.email = options.account
                pv.password = options.password
            self.accountviews.insert(0, pv)

    def reload(self):
        self.accountviews = []
        #TODO
        pass

    def getAllaccountviews(self):
        #TODO
        pass

    def getAvailableaccountviews(self):
        #TODO
        return self.accountviews
        pass

    def signingToAccount(self, accountview):
        #TODO
        pass

    def loadAccount(self, accountview, core):
        #TODO
        return aMSNAccount(accountview, core)

    def unloadAccount(self, amsnAccount):
        #TODO: unlock the Account
        pass


def elementToDict(element):
    """ Converts an XML Element into a proper Account dictionary """
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
