#!/usr/bin/python

import etk

cols = 1
rows = 2

#TODO: use stock_id
helpImage = etk.Image()
helpImage.set_from_file('help-browser.png')

def giveHelp(menu):
    print 'Sorry! :)'

t = etk.Table(cols=cols, rows=rows, homogeneous=etk.Table.NOT_HOMOGENEOUS)


mb = etk.MenuBar()
menuFileButton = etk.MenuItem(label='File')
menuHelpButton = etk.MenuItemImage(label='Help!')
menuHelpButton.image = helpImage #this image won't be displayed in the menubar
menuHelpButton.on_activated(giveHelp) #this event is not triggered
menuSeparator = etk.MenuItemSeparator()

#MenuFile
menuFile = etk.Menu()

menuCheckButton = etk.MenuItem(label='Menu Check buttons')
menuRadioButton = etk.MenuItem(label='Menu Radio buttons')
menuNeedHelpButton = etk.MenuItemImage(label='Help')
menuNeedHelpButton.image = helpImage
menuNeedHelpButton.on_activated(giveHelp)
menuQuit = etk.MenuItem(label='quit')

#Fill the file menu:
menuFile.append(menuRadioButton)
menuFile.append(menuCheckButton)
menuFile.append(menuSeparator)
menuFile.append(menuNeedHelpButton)
menuFile.append(menuQuit)
menuFileButton.submenu = menuFile



#Menu Check
submenuCheck = etk.Menu()
check1 = etk.MenuItemCheck(label='a check menu item')
check2 = etk.MenuItemCheck(label='a second menu item', active=True)
submenuCheck.append(check1)
submenuCheck.append(check2)
menuCheckButton.submenu = submenuCheck


#Menu Radio
submenuRadio = etk.Menu()
radio1 = etk.MenuItemRadio(fromWidget=None, label='choice 1')
radio2 = etk.MenuItemRadio(fromWidget=radio1, label='choice 2')
radio3 = etk.MenuItemRadio(fromWidget=radio1, label='choice 3')
submenuRadio.append(radio1)
submenuRadio.append(radio2)
submenuRadio.append(radio3)
menuRadioButton.submenu = submenuRadio

print 'o o'
radio1.group_get()
print ' -'

mb.append(menuFileButton)
mb.append(menuSeparator) #this one is not shown
mb.append(menuHelpButton)

t.attach(mb, 0, 0, 0, 0, etk.Table.FILL|etk.Table.HEXPAND, 0, 0)

b = etk.ToggleButton(label='Da Huge Toggle Button')
t.attach_default(b, 0, 0, 1, 1)


w = etk.Window(title="Testing menus!", size_request=(300, 300), child=t)
w.show_all()

def on_destroyed(obj):
    etk.main_quit()
w.connect("destroyed", on_destroyed)
menuQuit.on_activated(on_destroyed)


etk.main()
