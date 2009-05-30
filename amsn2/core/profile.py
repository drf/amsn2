
import os
import xml.etree.ElementTree
import xml.parsers.expat
import __builtin__

class aMSNProfilesList(object):
    """ aMSNProfilesList : Object representing profiles.xml """
    def __init__(self, profiles_dir):
        self.path = os.path.join(profiles_dir, "profiles.xml")
        self.updateProfilesList()

    def updateProfilesList(self):
        """ Reads the content of profiles.xml """
        if os.access(self.path, os.F_OK):
            profiles_file = file(self.path, "r")

            self.tree = xml.etree.ElementTree.ElementTree(file=profiles_file)

            profiles_file.close()

            self.root_element = self.tree.getroot()
        else :
            self.root_element = xml.etree.ElementTree.Element("aMSNProfilesList")

            self.tree = xml.etree.ElementTree.ElementTree(element =
                                                          self.root_element)

    def setProfileKey(self, profile_name, key, value):
        self.updateProfilesList()
        if self.ProfileIsListed(profile_name):
            profile_element = self.root_element.find(profile_name.replace("@", "_"))
            self.root_element.remove(profile_element)
            profile_dict = elementToDict(profile_element)

            if profile_dict.has_key(key):
                profile_dict[key] = value
                profile_element = dictToElement(profile_name.replace("@", "_"), profile_dict)
                self.root_element.append(profile_element)
                self.saveProfilesList()
            else:
                raise ProfileKeyNotListedError

    def getProfileKey(self, profile_name, key, default=None):
        self.updateProfilesList()
        if self.ProfileIsListed(profile_name):
            profile_element = self.root_element.find(profile_name.replace("@", "_"))
            profile_dict = elementToDict(profile_element)

            try:
                return profile_dict[key]
            except KeyError:
                return default
        else:
            return default

    def addProfile(self, profile, attributes_dict):
        """ Adds a profile section in profiles.xml """
        self.updateProfilesList()
        if self.ProfileIsListed(profile.email) is False:
            profile_element = dictToElement(profile.email.replace("@","_"), attributes_dict)
            self.root_element.append(profile_element)
            self.saveProfilesList()

    def deleteProfile(self, profile):
        """ Deletes a profile section from profiles.xml """
        self.updateProfilesList()
        for profile_element in self.root_element :
            if profile_element.tag == profile.email.replace("@","_"):
                self.root_element.remove(profile_element)
        self.saveProfilesList()

    def getAllProfilesNames(self):
        """ Returns a list of all profiles' email addresses """
        self.updateProfilesList()
        names_list = []

        for profile_element in self.root_element:
            profile_dict = elementToDict(profile_element)
            names_list.append(profile_dict["email"])

        return names_list

    def ProfileIsListed(self, profile_name):
        """ Returns True if the profile is in profiles.xml """
        return (profile_name in self.getAllProfilesNames())

    def saveProfilesList(self):
        """ Dumps aMSNProfilesList XML tree into profiles.xml """
        return self.tree.write(self.path)

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

class aMSNSmileyConfiguration(object):
    """ aMSNSmileyCinfiguration : A smiley object for profiles."""
    def __init__(self, profile, smiley, config_dict):
        """ config_dict must be a dictionary of configurations ("option": value, ...),
            the "shortcut" and "image" keys are mandatory."""
        self._profile = profile
        self._smiley = smiley
        self.config = config_dict
        self.config["valid"] = self.smileyIsValid()

    def smileyIsValid(self):
        """ Checks whether a shortcut and a image file are defined 
            and if the image file is accessible. Accordingly sets the "valid" key"""
        if self.config.has_key("shortcut") and self.config.has_key("image") :
            self.image_path = os.path.join(self._profile.directory, "smileys", self.config["image"])
            if os.access(self.image_path, os.R_OK) :
                return True
        return False

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
    def __init__(self, email, profiles_dir):
        self.email = email
        self.username = self.email
        self.alias = self.email
        self.password = None
        self.account = None
        self.presence = 'online'
        self.directory = os.path.join(profiles_dir, self.email)
        self.config = aMSNProfileConfiguration(self)
        ###self.plugins_configs must be a dictionary like {"Plugin1_name":aMSNPluginConfiguration(self,"Plugin1_name",{"option1":123}),
        ###                                        "Plugin2_name":aMSNPluginConfiguration(self,"Plugin2_name",{"option1":"sdda","option2":345})
        ###                                        }
        self.plugins_configs = {}
        ###self.smileys_configs must be a dictionary like {"Smiley1_name":aMSNSmileyConfiguration(self,"Smiley1_name",{"shortcut":";D", "image":image_file_name}),
        ###                                        "Smiley2_name":.....
        ###                                        }
        self.smileys_configs = {}

    def isLocked(self):
        """ Returns whether the profile is locked or not"""
        return False

    def lock(self):
        """ Locks a profile to avoid concurrent access to it from multiple instances """
        pass

    def unlock(self):
        """ Unlocks a profile to allow other instances to acces it """
        pass

    def remove_dir(self):
        """ Removes profile's directory from disk """

        for root, dirs, files in os.walk(self.directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        try:
            os.rmdir(self.directory)
        except:
            pass

    def getConfigKey(self, key, default = None):
        return self.config.getKey(key, default)

    def setConfigKey(self, key, value):
        return self.config.setKey(key, value)

    def getPluginKey(self, plugin_name, key, default = None):
        try:
            return self.plugins_configs[plugin_name].getKey(key, default)
        except KeyError:
            return default

    def setPluginKey(self, plugin_name, key, value):
        try:
            self.plugins_configs[plugin_name].setKey(key, default)
            return True
        except KeyError:
            return False

    def addPlugin(self, plugin_name, plugin_config_dict={}):
        self.plugins_configs[plugin_name] = \
            aMSNPluginConfiguration(self, plugin_name, plugin_config_dict)

    def removePlugin(self, plugin_name):
        return self.plugins_configs.pop(plugin_name, None)

    def getSmileyKey(self, plugin_name, key, default = None):
        try:
            return self.plugins_configs[plugin_name].getKey(key, default)
        except KeyError:
            return default

    def setSmileyKey(self, plugin_name, key, value):
        try:
            self.plugins_configs[plugin_name].setKey(key, default)
            return True
        except KeyError:
            return False

    def addSmiley(self, smiley_name, smiley_config_dict={"shortcut":"dummy", "image":"dummy"}):
        self.smileys_configs[smiley_name] = \
            aMSNSmileyConfiguration(self, smiley_name, smiley_config_dict)

    def removeSmiley(self, smiley_name):
        return self.smileys_configs.pop(smiley_name, None)


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

        try :
            os.makedirs(self._profiles_dir, 0777)
        except :
            pass

        self.profiles_list = aMSNProfilesList(self._profiles_dir)

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
            new_profile = aMSNProfile(email, self._profiles_dir)
            self.profiles[email] = new_profile

        return self.getProfile(email)

    def createProfile(self, email):
        """ Creates a profile and stores it on disk and adds it to the current instance """
        new_profile = self.addProfile(email)
        self.saveProfile(new_profile)
        return self.getProfile(email)

    def removeProfile(self, profile, and_delete=False):
        """ Removes a profile from the current instance of aMSN """
        if self.profileExists(profile.email):
            del self.profiles[profile.email]

        self.profiles_list.deleteProfile(profile)

        if and_delete == True:
            self.deleteProfile(profile)

    def deleteProfile(self, profile):
        """ Removes a profile from the current instance of aMSN and deletes it from disk """
        profile.remove_dir()

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

        plugins = profile.plugins_configs
        plugins_section = xml.etree.ElementTree.Element("Plugins")

        for plugin_name, plugin in plugins.iteritems():
            plugin_section = dictToElement(plugin_name, plugin.config)
            plugins_section.append(plugin_section)

        smileys = profile.smileys_configs
        smileys_section = xml.etree.ElementTree.Element("Smileys")

        for smiley_name, smiley in smileys.iteritems():
            smiley_section = dictToElement(smiley_name, smiley.config)
            smileys_section.append(smiley_section)

        root_section = xml.etree.ElementTree.Element("aMSNProfile")

        settings_section.append(config_section)
        settings_section.append(plugins_section)
        settings_section.append(smileys_section)
        root_section.append(settings_section)

        xml_tree = xml.etree.ElementTree.ElementTree(root_section)

        profile_dir = os.path.join(self._profiles_dir, profile.email)

        try :
            os.makedirs(profile_dir, 0777)
            os.makedirs(os.path.join(profile_dir, "smileys"), 0777)
            os.makedirs(os.path.join(profile_dir, "displaypics"), 0777)
            os.makedirs(os.path.join(profile_dir, "logs"), 0777)
            ## Other directories here
        except :
            pass

        profile_path = os.path.join(self._profiles_dir, profile.email, "config.xml")
        profile_file = file(profile_path, "w")
        xml_tree.write(profile_file)
        profile_file.close()

        list_opts={"email":profile.email,
                   "auto_connect":False
                   }
        self.profiles_list.addProfile(profile, list_opts)

    def saveAllProfiles(self):
        for profile in self.getAllProfiles():
            self.saveProfile(profile)

    def loadAllProfiles(self):
        """ Loads all profiles from disk """
        profiles_names = self.profiles_list.getAllProfilesNames()

        for profile_name in profiles_names :
            profile_file_path = os.path.join(self._profiles_dir, \
                                             profile_name, \
                                             "config.xml")
            if os.path.exists(profile_file_path) is False:
                continue

            ### Prepares XML Elements
            root_tree = xml.etree.ElementTree.parse(profile_file_path)
            settings = root_tree.find("Settings")
            settings_tree = xml.etree.ElementTree.ElementTree(settings)
            configs = settings_tree.find("Configurations")
            settings.remove(configs)
            plugins = settings_tree.find("Plugins")
            settings.remove(plugins)
            smileys = settings_tree.find("Smileys")
            settings.remove(smileys)

            ### Loads Settings
            settings_dict = elementToDict(settings)
            profile = aMSNProfile(settings_dict['email'], self._profiles_dir)
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

            for plugin_name, plugin_config_dict in plugins_dict.iteritems():
                profile.addPlugin(plugin_name, plugin_config_dict)

            ### Loads Smileys
            smileys_dict = {}
            for smiley_element in smileys:
                smileys_dict[smiley_element.tag] = elementToDict(smiley_element)

            for smiley_name, smiley_config_dict in smileys_dict.iteritems():
                profile.addSmiley(smiley_name, smiley_config_dict)

            ### Finally loads the Profile
            self.profiles[profile.email] = profile


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
