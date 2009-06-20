import os
import __builtin__
"""ElementTree independent from the available distribution"""
try:
    from xml.etree.cElementTree import *
except ImportError:
    try:
        from cElementTree import *
    except ImportError:
        from elementtree.ElementTree import *
from views import AccountView
from views import StringView

class aMSNAccount(object):
    """ aMSNAccount : a Class to represent an aMSN account
    This class will contain all settings relative to an account
    and will store the protocol and GUI objects
    """
    #TODO: use the personnal info stuff instead of the view
    def __init__(self, core, accountview, account_dir):
        """
        @type core: aMSNCore
        @type accountview: AccountView
        @type account_dir: str
        """

        self.view = accountview
        self.account_dir = account_dir
        self.do_save = accountview.save
        self.backend_manager = core._backend_manager
        self.lock()
        self.load()

    def signOut(self):
        if self.do_save:
            self.save()
        self.unlock()

    def lock(self):
        #TODO
        pass

    def unlock(self):
        #TODO
        pass

    def load(self):
        #TODO:
        self.config = self.backend_manager.loadConfig(self)

    def save(self):
        if not os.path.isdir(self.account_dir):
             os.makedirs(self.account_dir, 0700)
        self.backend_manager.saveConfig(self, self.config)
        #TODO: integrate with personnalinfo
        if self.view is not None and self.view.email is not None:
            root_section = Element("aMSNAccount")
            #email
            emailElmt = SubElement(root_section, "email")
            emailElmt.text = self.view.email
            #nick
            nick = str(self.view.nick)
            nickElmt = SubElement(root_section, "nick")
            nickElmt.text = nick
            #presence
            presenceElmt = SubElement(root_section, "presence")
            presenceElmt.text = self.view.presence
            #password
            if self.view.save_password:
                passwordElmt = self.backend_manager.setPassword(self.view.password, root_section)
                passwordElmt.text = self.view.password
            #dp
            #TODO ask the backend
            dpElmt = SubElement(root_section, "dp",
                                backend='DefaultBackend')
            #TODO

            #TODO: save or not, preferred_ui
            #
            #save password
            savePassElmt = SubElement(root_section, "save_password")
            savePassElmt.text = str(self.view.save_password)
            #autologin
            autologinElmt = SubElement(root_section, "autoconnect")
            autologinElmt.text = str(self.view.autologin)
            #TODO: backend for config/logs/...

            accpath = os.path.join(self.account_dir, "account.xml")
            xml_tree = ElementTree(root_section)
            xml_tree.write(accpath, encoding='utf-8')


class aMSNAccountManager(object):
    """ aMSNAccountManager : The account manager that takes care of storing
    and retreiving all the account.
    """
    def __init__(self, core, options):
        self._core = core
        if os.name == "posix":
            self._accounts_dir = os.path.join(os.environ['HOME'], ".amsn2")
        elif os.name == "nt":
            self._accounts_dir = os.path.join(os.environ['USERPROFILE'], "amsn2")
        else:
            self._accounts_dir = os.path.join(os.curdir, "amsn2_accounts")

        try :
            os.makedirs(self._accounts_dir, 0700)
        except :
            pass

        self.reload()

        if options.account is not None:
            pv = [p for p in self.accountviews if p.email == options.account]
            if pv:
                pv = pv[0]
                self.accountviews.remove(pv)
            else:
                pv = AccountView()
                pv.email = options.account
                pv.password = options.password
            self.accountviews.insert(0, pv)

    def reload(self):
        self.accountviews = []
        for root, dirs, files in os.walk(self._accounts_dir):
            account_dirs = dirs
            break
        for account_dir in account_dirs:
            accv = self.loadAccount(os.path.join(self._accounts_dir, account_dir))
            if accv:
                self.accountviews.append(accv)


    def loadAccount(self, dir):
        accview = None
        accpath = os.path.join(dir, "account.xml")
        accfile = file(accpath, "r")
        root_tree = ElementTree(file=accfile)
        accfile.close()
        account = root_tree.getroot()
        if account.tag == "aMSNAccount":
            accview = AccountView()
            #email
            emailElmt = account.find("email")
            if emailElmt is None:
                return None
            accview.email = emailElmt.text
            #nick
            nickElmt = account.find("nick")
            if nickElmt is None:
                return None
            if nickElmt.text:
                accview.nick.appendText(nickElmt.text)
            #TODO: parse...
            #presence
            presenceElmt = account.find("presence")
            if presenceElmt is None:
                return None
            accview.presence = presenceElmt.text
            #password
            passwordElmt = account.find("password")
            if passwordElmt is None:
                accview.password = None
            else:
                accview.password = self.core._backend_manager.getPassword(passwordElmt)
            #save_password
            savePassElmt = account.find("save_password")
            if savePassElmt.text == "False":
                accview.save_password = False
            else:
                accview.save_password = True
            #autoconnect
            saveAutoConnect = account.find("autoconnect")
            if saveAutoConnect.text == "False":
                accview.autologin = False
            else:
                accview.autologin = True
            #TODO: use backend & all
            #dp
            dpElmt = account.find("dp")
            #TODO

            #TODO: preferred_ui ?

            accview.save = True
        return accview



    def getAllAccountViews(self):
        return self.accountviews

    def getAvailableAccountViews(self):
        return [v for v in self.accountviews if not self.isAccountLocked(v)]

    def signinToAccount(self, accountview):
        """
        @type accountview: AccountView
        @rtype: aMSNAccount
        """
        if accountview.save:
            # save the backend type in the account?
            self._core._backend_manager.switchToBackend('defaultbackend')
            accdir = os.path.join(self._accounts_dir,
                                  accountNameToDirName(accountview.email))
        else:
            # TODO: accdir should be a tmp dir
            accdir = None
        acc = aMSNAccount(self._core, accountview, accdir)
        acc.lock()
        return acc

    def isAccountLocked(self, accountview):
        """
        @type accountview: AccountView
        @rtype: bool
        @return: True if accountview is locked
        """

        #TODO
        return False

def accountNameToDirName(acc):
    """
    @type acc: str
    @param acc: account email
    @rtype: str
    @return: account email parsed to use as dir name
    """

    #Having to do that just sucks
    return acc.lower().strip().replace("@","_at_")

