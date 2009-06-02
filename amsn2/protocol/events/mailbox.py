
import papyon
import papyon.event

class MailboxEvents(papyon.event.MailboxEventInterface):
    def __init__(self, client, amsn_core):
        self._amsn_core = amsn_core
        papyon.event.MailboxEventInterface.__init__(self, client)

    def on_mailbox_unread_mail_count_changed(self, unread_mail_count,
                                                   initial=False):
        """The number of unread mail messages"""
        pass

    def on_mailbox_new_mail_received(self, mail_message):
        """New mail message notification"""
        pass
