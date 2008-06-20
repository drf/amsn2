#from amsn2.gui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_chatWindow import Ui_ChatWindow
    
class aMSNChatWindow(QWidget):
    def __init__(self, Parent=None):
        QWidget.__init__(self, Parent)
        # TODO: Init chat window code from amsn core here
        
        self.ui = Ui_ChatWindow()
        self.ui.setupUi(self)
        
        self.loadEmoticonList()
        
        QObject.connect(self.ui.inputWidget, SIGNAL("textChanged()"), self.processInput)
        QObject.connect(self.ui.actionInsert_Emoticon, SIGNAL("triggered()"), self.showEmoticonList)
        """ These connections needs to be revisited, since they should probably point
        to an interface method """
        self.enterShortcut = QShortcut("Enter", self.ui.inputWidget)
        QObject.connect(self.enterShortcut, SIGNAL("activated()"), self.sendMessage)
        
        QObject.connect(self.ui.actionNudge, SIGNAL("triggered()"), self.nudge)
        

    def processInput(self):
        """ Here we process what is inside the widget... so showing emoticon
        and similar stuff"""
        
        QObject.disconnect(self.ui.inputWidget, SIGNAL("textChanged()"), self.processInput)
        
        self.text = QString(self.ui.inputWidget.toHtml())
                
        for emoticon in self.emoticonList:
            if self.text.contains(emoticon) == True:
                print emoticon
                self.text.replace(emoticon, "<img src=\"throbber.gif\" />")
                
        self.ui.inputWidget.setHtml(self.text)
        self.ui.inputWidget.moveCursor(QTextCursor.End)
        
        QObject.connect(self.ui.inputWidget, SIGNAL("textChanged()"), self.processInput)
        
    def sendMessage(self):
        print "To Implement"
        
    def loadEmoticonList(self):
        self.emoticonList = QStringList()
        
        """ TODO: Request emoticon list from amsn core, maybe use a QMap to get the image URL? """
        
        """ TODO: Discuss how to handle custom emoticons. We have to provide an option
        to change the default icon theme, this includes standard emoticons too.
        Maybe qrc? """
        
        self.emoticonList << ";)" << ":)" << "EmOtIcOn"
        
    def showEmoticonList(self):
        """ Let's popup emoticon selection here """
        print "Guess what? No emoticons. But I'll put in a random one for you"
        self.appendImageAtCursor("throbber.gif")
        
    def nudge(self):
        print "Driiiiin!!!"
        
    def appendTextAtCursor(self, text):
        self.ui.inputWidget.textCursor().insertHtml(str(text))
        
    def appendImageAtCursor(self, image):
        self.ui.inputWidget.textCursor().insertHtml(QString("<img src=\"" + str(image) + "\" />"))
        
