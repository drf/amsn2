"""ElementTree independent from the available distribution"""
try:
    from xml.etree.cElementTree import *
except ImportError:
    try:
        from cElementTree import *
    except ImportError:
        from elementtree.ElementTree import *

def getPassword(passwdElmt):
    return passwdElmt.text

def setPassword(password, root_section):
    elmt = SubElement(root_section, "password", backend='DefaultBackend')
    elmt.text = password
    return elmt
