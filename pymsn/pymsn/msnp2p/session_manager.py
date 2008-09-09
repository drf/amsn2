# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2007 Ali Sabil <ali.sabil@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from pymsn.msnp2p.transport import *
from pymsn.msnp2p.exceptions import *
from pymsn.msnp2p.SLP import *
from pymsn.msnp2p.session import IncomingP2PSession
from pymsn.msnp2p.constants import SLPContentType, SLPRequestMethod

import pymsn.profile

import gobject
import weakref
import logging

__all__ = ['P2PSessionManager']

logger = logging.getLogger('msnp2p:session-manager')

class P2PSessionManager(gobject.GObject):
    __gsignals__ = {
            "incoming-session" : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,))
    }

    def __init__(self, client):
        """Initializer"""
        gobject.GObject.__init__(self)

        self._client = client
        self._sessions = weakref.WeakValueDictionary() # session_id => session
        self._transport_manager = P2PTransportManager(self._client)
        self._transport_manager.connect("blob-received",
                lambda tr, blob: self._on_blob_received(blob))
        self._transport_manager.connect("blob-sent",
                lambda tr, blob: self._on_blob_sent(blob))

    def _register_session(self, session):
        self._sessions[session.id] = session

    def _unregister_session(self, session):
        del self._sessions[session.id]

    def _blob_to_session(self, blob):
        # Check to see if it's a signaling message
        if blob.session_id == 0:
            blob.data.seek(0, 0)
            slp_data = blob.data.read()
            blob.data.seek(0, 0)
            try:
                message = SLPMessage.build(slp_data)
            except ParseError:
                logger.warning('Received blob with SessionID=0 and non SLP data')
                raise SLPError("Non SLP data for blob with null sessionID")
            session_id = message.body.session_id

            # Backward compatible with older clients that use the call-id
            # for responses
            if session_id == 0:
                call_id = message.call_id
                for session in self._sessions.itervalues():
                    if session.call_id == call_id:
                        return session
                # Couldn't find a session for the call id we received
                return None
            if session_id in self._sessions:
                return self._sessions[session_id]
            # Session doesn't exist
            return None
        else:
            session_id = blob.session_id
            if session_id in self._sessions:
                return self._sessions[blob.session_id]
            else:
                raise SLPSessionError("Unknown session")

    def _on_blob_received(self, blob):
        try:
            session = self._blob_to_session(blob)
        except SLPError:
            # If the blob has a null session id but a badly formed SLP
            # Then we should do nothing. The official client doesn't answer.
            # We can't send a '500 Internal Error' response since we can't
            # parse the SLP, so we don't know who to send it to, or the call-id, etc...
            return
        except SLPSessionError:
            # This means that we received a data packet for an unknown session
            # We must RESET the session just like the official client does
            # TODO send a TLP
            return

        new_session = session is None

        # The session could not be found, create a new one if necessary
        if session is None:
            # Parse the SLP message. We know it's an SLP because if it was a data packet
            # we would have received a ProtocolError exception
            blob.data.seek(0, 0)
            slp_data = blob.data.read()
            blob.data.seek(0, 0)

            # No need to 'try', if it was invalid, we would have received an SLPError
            message = SLPMessage.build(slp_data)
            session_id = message.body.session_id

            logger.info("blob has SLP (%d):\n%s" % (session_id, message))

            # Make sure the SLP has a session_id, otherwise, it means it's invite
            # if it's a signaling SLP and the call-id could not be matched to
            # an existing session
            if session_id == 0:
                # TODO send a 500 internal error
                return

            # If there was no session then create one only if it's an INVITE
            if isinstance(message, SLPRequestMessage) and \
                    message.method == SLPRequestMethod.INVITE:
                # Find the contact we received the message from
                contacts = self._client.address_book.contacts.\
                           search_by_network_id(pymsn.profile.NetworkID.MSN).\
                           search_by_account(message.frm)
                if len(contacts) == 0:
                    peer = pymsn.profile.Contact(id=0, 
                                                 network_id=pymsn.profile.NetworkID.MSN, 
                                                 account=message.frm, 
                                                 display_name=message.frm)
                else:
                    peer = contacts[0]

                # Create the session depending on the type of the message
                if isinstance(message.body, SLPSessionRequestBody):
                    try:
                        session = IncomingP2PSession(self, peer, session_id, message)
                    except SLPError:
                        #TODO: answer with a 603 Decline ?
                        return 
                #elif isinstance(message.body, SLPTransferRequestBody):
                #    pass  
            else:
                logger.warning('Received initial blob with SessionID=0 and non INVITE SLP data')
                #TODO: answer with a 500 Internal Error
                return None

        # The session should be notified of this blob
        session._on_blob_received(blob)

        # emit the new session signal only after the session got notified of this blob
        # if one of the functions connected to the signal ends the session it needs to
        # first know its initial INVITE before knowing about it's BYE
        if new_session:
            logger.info("Creating new incomming session")
            self.emit("incoming-session", session)

    def _on_blob_sent(self, blob):
        session = None
        try:
            session = self._blob_to_session(blob)
        except SLPError, e:
            # Something is fishy.. we shouldn't have to send anything abnormal..
            logger.warning("Sent a bad message : %s" % (e))
            session = None
        except SLPSessionError, e:
            # May happen when we close the session
            pass

        if session is None:
            return
        session._on_blob_sent(blob)

gobject.type_register(P2PSessionManager)
