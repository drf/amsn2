import os
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xml.parsers.expat
import __builtin__
from views import AccountView
from views import StringView

class aMSNAccount(object):
    """ aMSNAccount : a Class to represent an aMSN account
    This class will contain all settings relative to an account
    and will store the protocol and GUI objects
    """
    #TODO: use the personnal info stuff instead of the view
    def __init__(self, core, accountview, account_dir):
        self.view = profileview
        self.account_dir = account_dir
        self.password_backend = "default"
        self.dp_backend = "default"
        self.do_save = accountview.save

        self.lock()
        #TODO

    def signOut(self):
        self.save()
        self.unlock()

    def lock(self):
        #TODO
        pass

    def unlock(self):
        #TODO
        pass

    def load(self):
        #TODO
        pass

    def save(self):
        if self.view is not None and self.view.email is not None:
            root_section = Element("aMSNAccount")
            #email
            emailElmt = SubElement(root_section, "email")
            emailElmt.text = self.view.email
            #nick
            nick = self.view.nick.toString()
            nickElmt = SubElement(root_section, "nick")
            nickElmt.text = nick
            #status
            statusElmt = SubElement(root_section, "status")
            statusElmt.text = self.view.status
            #password
            #TODO ask the backend
            passwordElmt = SubElement(root_section, "dp",
                                      backend=self.password_backend)
            passwordElmt.text = self.view.password
            #dp
            dpElmt = SubElement(root_section, "dp",
                                  backend=self.dp_backend)
            #TODO

            #TODO: save or not, preferred_ui
            #TODO: backend for config/logs/...

            if not os.path.isdir(self.account_dir):
                os.makedirs(self.account_dir, 0700)
            accpath = os.path.join(self.account_dir, "account.xml")
            xml_tree = ElementTree(root_section)
            xml_tree.write(accpath)


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
            os.makedirs(self._accounts_dir, 0700)
        except :
            pass

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
        for root, dirs, files in os.walk(self._accounts_dir):
            account_dirs = dirs
            break

        for account_dir in account_dirs:
            self.accountviews.append(self.loadAccount(account_dir))


    def loadAccount(self, dir):
        accview = None
        accpath = os.path.join(dir, "account.xml")
        root_tree = parse(accpath)
        account = root_tree.find("aMSNAccount")
        if account is not None:
            accview = Accountview()
            #email
            emailElt = account.find("email")
            accview.email = text
            #nick
            nickElmt = account.find("nick")
            accview.nick.appendText(nickElmt.text)
            #TODO: parse...
            #status
            statusElmt = account.find("status")
            accview.status = statusElmt.text
            #password
            passwordElmt = account.find("password")
            accview.password = passwordElmt.text
            #TODO: use backend & all
            #dp
            dpElt = account.find("dp")
            #TODO

            #TODO: preferred_ui ?

            accview.save = True
        return accview



    def getAllAccountViews(self):
        return self.accountviews

    def getAvailableAccountViews(self):
        return [v for v in self.accountviews if not self.isAccountLocked(v)]
        pass

    def signingToAccount(self, accountview):
        accdir = os.path.join(self._accounts_dir,
                              accountNameToDirName(accountview.email))
        acc = aMSNAccount(self.core, accountview, accdir)
        return acc

    def isAccountLocked(self, accountview):
        #TODO
        return False

def accountNameToDirName(acc):
    #Having to do that just sucks
    str = acc.lower().strip().replace("@","_at_");

