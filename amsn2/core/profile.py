class aMSNProfileConfiguration(object):
    def __init__(self, profile):
        self._profile = profile
        self.config = {"ns_server":'messenger.hotmail.com', "ns_port":1863}
        
    def getConfigKey(self, key, default = None):
        try:
            value = self.config[key]
        except KeyError:
            value = default
        return value
        
    def setConfigKey(self, key, value):
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
    
    def isLocked(self):
        """ Returns whether the profile is locked or not"""
        return False

    def lock(self):
        """ Locks a profile to avoid concurrent access to it from multiple instances """
        pass
    
    def unlock(self):
        """ Unlocks a profile to allow other instances to acces it """
        pass

    def connect(self):
        pass

class aMSNProfileManager(object):
    """ aMSNProfileManager : The profile manager that takes care of storing
    and retreiving all the profiles for our users.
    """
    def __init__(self):
        self.profiles = {}
        pass


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
        # TODO : Write to disk info about the current profile
        return addProfile(email)

    def removeProfile(self, profile):
        """ Removes a profile from the current instance of aMSN """
        if self.profileExists(profile.email):
            del self.profiles[profile.email]
        

    def deleteProfile(self, profile):
        """ Removes a profile from the current instance of aMSN and deletes it from disk """
        # TODO : remove from disk
        return removeProfile(self, profile)
        

        
