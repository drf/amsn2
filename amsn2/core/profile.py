
import os
import xml.etree.ElementTree
import xml.parsers.expat
import __builtin__

class aMSNProfileConfiguration(object):
    def __init__(self, profile):
        self._profile = profile
        self.config = {"ns_server":'messenger.hotmail.com',
                       "ns_port":1863,
                       }
        
    def getKey(self, key, default = None):
        try:
            return self.config[key]
        except KeyError:
            return default
        
    def setKey(self, key, value):
        self.config[key] = value

class aMSNPluginConfiguration(object):
    """ aMSNProfilePlugin : A plugin object for profiles."""
    def __init__(self, profile, plugin, config_dict):
        """ config_dict must be a dictionary of configurations ("option": value, ...) """
        self._profile = profile
        self._plugin = plugin
        self.config = config_dict

    def getKey(self, key, default = None):
        try:
            return self.config[key]
        except KeyError:
            return default
        
    def setKey(self, key, value):
        self.config[key] = value

class aMSNProfile(object):
    """ aMSNProfile : a Class to represent an aMSN profile
    This class will contain all settings relative to a profile
    and will store the protocol and GUI objects    
    """
    def __init__(self, email):
        self.email = email
        self.username = self.email
        self.alias = self.email
        self.password = None
        self.account = None
        self.config = aMSNProfileConfiguration(self)
        ###self.plugins must be a dictionary like {"Plugin1_name":aMSNProfilePlugin(self,{"option1":123}),
        ###                                        "Plugin2_name":aMSNProfilePlugin(self,{"option1":"sdda","option2":345})
        ###                                        }
        self.plugin_configs = {}
    
    def isLocked(self):
        """ Returns whether the profile is locked or not"""
        return False

    def lock(self):
        """ Locks a profile to avoid concurrent access to it from multiple instances """
        pass
    
    def unlock(self):
        """ Unlocks a profile to allow other instances to acces it """
        pass

    def getConfigKey(self, key, default = None):
        return self.config.getKey(key, default)

    def setConfigKey(self, key, value):
        return self.config.setKey(key, value)

    def getPluginKey(self, plugin_name, key, default = None):
        try:
            return self.plugin_configs[plugin_name].getKey(key, default)
        except KeyError:
            return default

    def setPluginKey(self, plugin_name, key, value):
        try:
            self.plugin_configs[plugin_name].setKey(key, default)
            return True
        except KeyError:
            return False
    
    def addPlugin(self, plugin_name, plugin_config_dict):
        self.plugin_configs[plugin_name] = \
            aMSNPluginConfiguration(self, plugin_name, plugin_config_dict)
    
    def removePlugin(self, plugin_name):
        return self.plugins.pop(plugin_name, None)

class aMSNProfileManager(object):
    """ aMSNProfileManager : The profile manager that takes care of storing
    and retreiving all the profiles for our users.
    """
    def __init__(self):
        if os.name == "posix":
            self._profiles_dir = os.path.join(os.environ['HOME'], ".amsn2")
        elif os.name == "nt":
            self._profiles_dir = os.path.join(os.environ['USERPROFILE'], "amsn2")
        else:
            self._profiles_dir = os.path.join(os.curdir, "amsn2")
        self.profiles = {}
        self.loadAllProfiles()

    def profileExists(self, email):
        """ Checks whether a profile exists """
        return self.getProfile(email) is not None
    
    def getProfile(self, email):
        """ Get a profile object by email """
        try:
            profile = self.profiles[email]
        except KeyError:
            profile = None
        return profile

    def getAllProfiles(self):
        return self.profiles.values()

    def addProfile(self, email):
        """ Adds a profile to the current running instance of aMSN """
        if self.profileExists(email) is False:
            new_profile = aMSNProfile(email)
            self.profiles[email] = new_profile
        
        return self.getProfile(email)

    def createProfile(self, email):
        """ Creates a profile and stores it on disk and adds it to the current instance """
        new_profile = self.addProfile(email)
        self.saveProfile(new_profile)
        return new_profile

    def removeProfile(self, profile):
        """ Removes a profile from the current instance of aMSN """
        if self.profileExists(profile.email):
            del self.profiles[profile.email]
        
    def deleteProfile(self, profile):
        """ Removes a profile from the current instance of aMSN and deletes it from disk """
        profile_dir_path = os.path.join(os.environ['HOME'], ".amsn2", "profiles", profile.email)
        
        for root, dirs, files in os.walk(profile_dir_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        try:
            os.rmdir(profile_dir_path)
        except:
            pass

        return self.removeProfile(profile)
    
    def saveProfile(self, profile):
        """ Stores a profile on disk """        
        config = profile.config.config
            
        config_section = dictToElement("Configurations", config)
        
        settings = {"email":profile.email,
                    "username":profile.username,
                    "alias":profile.alias,
                    "password":profile.password,
                    "account":profile.account
                    }
        
        if profile.password == None :
            settings["password"] = ""
        if profile.account == None :
            settings["account"] = ""
        
        settings_section = dictToElement("Settings", settings)
        
        plugins = profile.plugins
        
        plugins_section = xml.etree.ElementTree.Element("Plugins")
        
        for plugin_name, plugin in plugins.iteritems():
            plugin_section = dictToElement(plugin_name, plugin.config)
            plugins_section.append(plugin_section)
        
        root_section = xml.etree.ElementTree.Element("aMSNProfile")
        
        settings_section.append(config_section)
        settings_section.append(plugins_section)
        root_section.append(settings_section)
        
        xml_tree = xml.etree.ElementTree.ElementTree(root_section)
        
        profile_dir = os.path.join(self._profiles_dir, profile.email)
        
        try :
            os.makedirs(profile_dir, 0777)
            os.makedirs(os.path.join(profile_dir, "smileys"), 0777)
            os.makedirs(os.path.join(profile_dir, "displaypics"), 0777)
            ## Other directories here
        except :
            pass
        
        profile_path = os.path.join(self._profiles_dir, profile.email, "settings.xml")
        profile_file = file(profile_path, "w")
        xml_tree.write(profile_file)
        profile_file.close()
    
    def loadAllProfiles(self):
        """ Loads all profiles from disk """  
        try :
            os.makedirs(self._profiles_dir, 0777)
        except :
            pass
        
        for root, dirs, files in os.walk(self._profiles_dir):
            profiles_dirs = dirs
            ### To be extended
            break

        for profile_dir in profiles_dirs :
            profile_file_path = os.path.join(self._profiles_dir, profile_dir, "settings.xml")
            
            ### Prepares XML Elements
            root_tree = xml.etree.ElementTree.parse(profile_file_path)
            settings = root_tree.find("Settings")
            settings_tree = xml.etree.ElementTree.ElementTree(settings)
            configs = settings_tree.find("Configurations")
            settings.remove(configs)
            plugins = settings_tree.find("Plugins")
            settings.remove(plugins)
            
            ### Loads Settings
            settings_dict = elementToDict(settings) 
            profile = aMSNProfile(settings_dict['email'])
            profile.username = settings_dict['username']
            profile.alias = settings_dict['alias']
            profile.password = settings_dict['password']
            profile.account = settings_dict['account']
            profile.config = aMSNProfileConfiguration(profile)

            if profile.password == "" :
                profile.password = None
            if profile.account == "" :
                profile.account = None
                
            ### Loads Configurations
            configs_dict = elementToDict(configs)
            profile.config.config = configs_dict
            
            ### Loads Plugins
            plugins_dict = {}
            for plugin_element in plugins:
                plugins_dict[plugin_element.tag] = elementToDict(plugin_element)
            
            profile.plugins = {}
            for plugin_name, plugin_config_dict in plugins_dict.iteritems():
                profile.addPlugin(plugin_name, plugin_config_dict)
            
            ### Finally loads the Profile
            self.profiles[profile.email] = profile

def elementToDict(element):
    """ Converts an XML Element into a proper profile dictionary """
    def dictToTuple(name, dict):
        """ Converts a dictionary returned by expat XML parser into a proper tuple and adds it to a list ready for dict() """
        key = dict['name']
        type = dict['type']
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
        values.append(str(value))
        type_obj = __builtin__.type(value)
        types.append(str(type_obj)[7:-2])
    
    for key, type, value in zip(keys, types, values) :
        element = xml.etree.ElementTree.Element("entry", {"name":key, "type":type, "value":value})
        root_element.append(element)
    
    return root_element
