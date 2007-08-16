#!/usr/bin/env python

import pymsn
import pymsn.event

import logging
import gobject

logging.basicConfig(level=logging.DEBUG)

finished = False

def get_proxies():
    import urllib
    proxies = urllib.getproxies()
    result = {}
    if 'https' not in proxies and \
            'http' in proxies:
        url = proxies['http'].replace("http://", "https://")
        result['https'] = pymsn.Proxy(url)
    for type, url in proxies.items():
        if type == 'no': continue
        if type == 'https' and url.startswith('http://'):
            url = url.replace('http://', 'https://', 1)
        result[type] = pymsn.Proxy(url)
    return result


class ClientEvents(pymsn.event.ClientEventInterface):
    def on_client_state_changed(self, state):
        if state == pymsn.event.ClientState.CLOSED:
            self._client.quit()
        elif state == pymsn.event.ClientState.OPEN:
            self._client.profile.display_name = "Kimbix"
            self._client.profile.presence = pymsn.Presence.ONLINE
            self._client.profile.current_media = ("I listen to", "Nothing")
            #self._client.profile.personal_message = "Testing pymsn, and freeing the pandas!"
            gobject.timeout_add(5000, self._client.start_conversation)

    def on_client_error(self, error_type, error):
        print "ERROR :", error_type, " ->", error

class AnnoyingConversation(pymsn.event.ConversationEventInterface):
    def on_conversation_user_joined(self, contact):
        gobject.timeout_add(5000, self.annoy_user)

    def annoy_user(self):
        self._client.send_typing_notification()
        formatting = pymsn.TextFormat("Comic Sans MS", 
                                      pymsn.TextFormat.UNDERLINE | pymsn.TextFormat.BOLD,
                                      'FF0000')
        self._client.send_text_message("Let's free the pandas ! (testing pymsn)",
                                       formatting)
        #self._client.send_nudge()
        #self._client.send_typing_notification()
        #self._client.send_typing_notification()
        #self._client.send_typing_notification()
        return True

    def on_conversation_message_received(self, sender, message, formatting):
        print formatting

    def on_conversation_error(self, error_type, error):
        print "ERROR :", error_type, " ->", error

class Client(pymsn.Client):
    def __init__(self, account, quit, http_mode=False):
        server = ('messenger.hotmail.com', 1863)
        self.quit = quit
        self.account = account
        if http_mode:
            from pymsn.transport import HTTPPollConnection
            pymsn.Client.__init__(self, server, get_proxies(), HTTPPollConnection)
        else:
            pymsn.Client.__init__(self, server, proxies = get_proxies())
        ClientEvents(self)
        gobject.idle_add(self._connect)

    def _connect(self):
        self.login(*self.account)
        return False

    def start_conversation(self):
        contacts = self.address_book.contacts.\
                search_by_presence(pymsn.Presence.ONLINE)
        if len(contacts) == 0:
            print "No online contacts"
            return True
        else:
            for contact in contacts:
                #if contact.account == "im_a_jabber_monkey@hotmail.com":
                #if contact.account == "tp-butterfly@hotmail.com":
                if contact.account == "johann.prieur@gmail.com":
                    print "Inviting %s for a conversation" % contact.display_name
                    self.conv = pymsn.Conversation(self, [contact])
                    AnnoyingConversation(self.conv)
            return False

def main():
    import sys
    import getpass
    import signal

    if "--http" in sys.argv:
        http_mode = True
        sys.argv.remove('--http')
    else:
        http_mode = False

    if len(sys.argv) < 2:
        account = raw_input('Account: ')
    else:
        account = sys.argv[1]

    if len(sys.argv) < 3:
        passwd = getpass.getpass('Password: ')
    else:
        passwd = sys.argv[2]

    mainloop = gobject.MainLoop(is_running=True)

    def quit():
        mainloop.quit()

    def sigterm_cb():
        gobject.idle_add(quit)

    signal.signal(signal.SIGTERM, sigterm_cb)

    n = Client((account, passwd), quit, http_mode)

    while mainloop.is_running():
        try:
            mainloop.run()
        except KeyboardInterrupt:
            quit()

if __name__ == '__main__':
    main()
