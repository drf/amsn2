
import os
from amsn2.core.views import AccountView
import basebackend

"""ElementTree independent from the available distribution"""
try:
    from xml.etree.cElementTree import *
except ImportError:
    try:
        from cElementTree import *
    except ImportError:
        from elementtree.ElementTree import *
import os

class defaultaccountbackend(basebackend.basebackend):
    """
    Save/load the account informations, should be used from all the backends.
    """

    def __init__(self):
        if os.name == "posix":
            self.accounts_dir = os.path.join(os.environ['HOME'], ".amsn2")
        elif os.name == "nt":
            self.accounts_dir = os.path.join(os.environ['USERPROFILE'], "amsn2")
        else:
            self.accounts_dir = os.path.join(os.curdir, "amsn2_accounts")

        try :
            os.makedirs(self.accounts_dir, 0700)
        except :
            pass

    def loadAccount(self, email):
        accview = None
        self.createAccountFileTree(email)
        accpath = os.path.join(self.account_dir, "account.xml")
        accfile = file(accpath, "r")
        root_tree = ElementTree(file=accfile)
        accfile.close()
        account = root_tree.getroot()
        if account.tag == "aMSNAccount":
            accview = AccountView(self._core)
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
            #psm
            psmElmt = account.find("psm")
            if psmElmt is None:
                return None
            if psmElmt.text:
                accview.psm.appendText(psmElmt.text)
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
                accview.password = passwordElmt.text
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

    def loadAccounts(self):
        account_dirs = []
        for root, dirs, files in os.walk(self.accounts_dir):
            account_dirs = dirs
            break
        accountviews = []
        for account_dir in account_dirs:
            accv = self.loadAccount(os.path.join(self.accounts_dir, account_dir))
            if accv:
                accountviews.append(accv)
        return accountviews

    def createAccountFileTree(self, email):
        self.account_dir = os.path.join(self.accounts_dir, self._getDir(email))
        if not os.path.isdir(self.account_dir):
                os.makedirs(self.account_dir, 0700)
        self.dps_dir = os.path.join(self.account_dir, "displaypics")
        if not os.path.isdir(self.dps_dir):
                os.makedirs(self.dps_dir, 0700)

    def setAccount(self, email):
        self.createAccountFileTree(email)

    def saveAccount(self, amsn_account):
        if amsn_account.view is None or amsn_account.view.email is None:
            return false

        self.createAccountFileTree(amsn_account.view.email)
        amsn_account.backend_manager.saveConfig(amsn_account, amsn_account.config)
        #TODO: integrate with personnalinfo
        root_section = Element("aMSNAccount")
        #email
        emailElmt = SubElement(root_section, "email")
        emailElmt.text = amsn_account.view.email
        #nick
        nick = str(amsn_account.view.nick)
        nickElmt = SubElement(root_section, "nick")
        nickElmt.text = nick
        #psm
        psm = str(amsn_account.view.psm)
        psmElmt = SubElement(root_section, "psm")
        psmElmt.text = psm
        #presence
        presenceElmt = SubElement(root_section, "presence")
        presenceElmt.text = amsn_account.view.presence
        #password
        if amsn_account.view.save_password:
            passwdElmt = SubElement(root_section, "password")
            passwdElmt.text = amsn_account.view.password
        #dp
        #TODO ask the backend
        dpElmt = SubElement(root_section, "dp")
        #TODO

        #TODO: save or not, preferred_ui
        #
        #save password
        savePassElmt = SubElement(root_section, "save_password")
        savePassElmt.text = str(amsn_account.view.save_password)
        #autologin
        autologinElmt = SubElement(root_section, "autoconnect")
        autologinElmt.text = str(amsn_account.view.autologin)
        #TODO: backend for config/logs/...

        accpath = os.path.join(self.account_dir, "account.xml")
        xml_tree = ElementTree(root_section)
        xml_tree.write(accpath, encoding='utf-8')

    def removeAccount(self, email):
        accdir = os.path.join(self.accounts_dir, self._getDir(email))
        if os.path.isdir(accdir):
            for [root, subdirs, subfiles] in os.walk(accdir, False):
                for subfile in subfiles:
                    os.remove(os.path.join(root, subfile))
                for subdir in subdirs:
                    os.rmdir(os.path.join(root, subdir))
            os.rmdir(accdir)

    """ DPs """
    def getFileLocationDP(self, email, uid, shac):
        dir = os.path.join(self.dps_dir, self._getDir(email))
        if not os.path.isdir(dir):
            os.makedirs(dir, 0700)
        return os.path.join(dir, shac+".img")

    def _getDir(self, email):
        return email.lower().strip().replace("@","_at_")
