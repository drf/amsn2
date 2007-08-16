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

from pymsn.msnp2p.constants import *
from pymsn.msnp2p.SLP import *
from pymsn.msnp2p.transport import *
import pymsn.profile

import random
import base64

__all__ = ['MSNObjectTransferSession']

MAX_INT32 = 0x7fffffff
MAX_INT16 = 0x7fff

def _generate_id(max=MAX_INT32):
    """
    Returns a random ID.

        @return: a random integer between 1000 and sys.maxint
        @rtype: integer
    """
    return random.randint(1000, max)

def _generate_guid():
    bytes = [random.randrange(256) for i in range(16)]

    data1 = ("%02X" * 4) % tuple(bytes[0:4])
    data2 = ("%02X" * 2) % tuple(bytes[4:6])
    data3 = ("%02X" * 2) % tuple(bytes[6:8])
    data4 = ("%02X" * 2) % tuple(bytes[8:10])
    data5 = ("%02X" * 6) % tuple(bytes[10:])

    data3 = "4" + data3[1:]

    return "{%s-%s-%s-%s-%s}" % (data1, data2, data3, data4, data5)


class P2PSessionInvite(object):
    def __init__(self, client, session, slp_request):
        self._session = session
        self._request = slp_request

        contacts = client.address_book.contacts.\
                search_by_network_id(pymsn.profile.NetworkID.MSN).\
                search_by_account(slp_request.frm)
        if len(contacts) == 0:
            contact = pymsn.profile.Contact(id=0,
                    network_id=pymsn.profile.NetworkID.MSN,
                    account=account,
                    display_name=account)
        else:
            contact = contacts[0]
        self.frm = contact
        self.to = client.profile

    def accept(self):
        self._respond(200)

    def reject(self):
        self._respond(603)

    def _respond(self, status_code):
        response = SLPResponseMessage(status_code,
                to = self.frm.account,
                frm = self.to.account,
                branch = self._request.branch,
                cseq = self._request.cseq + 1,
                branch = self._request.branch,
                call_id = self._request.call_id)
        self._session._send_p2p_data(response)

class P2PSession(object):
    def __init__(self, client, peer, euf_guid="", application_id=0):
        """Initializer"""
        self._client = client
        self._peer = peer

        self._euf_guid = euf_guid
        self._application_id = application_id

        self._call_id = None
        self._session_id = None

        #FIXME: implement the transport manager and get rid of this
        self._transport = SwitchboardP2PTransport(self._client, self._peer)

    def invite(self, context):
        if self._call_id is None:
            self._call_id = _generate_guid()
        if self._session_id is None:
            self._session_id = _generate_id()

        body = SLPMessageBody(SLPContentType.SESSION_REQUEST)
        body.add_header('EUF-GUID', self._euf_guid)
        body.add_header('SessionID', self._session_id)
        body.add_header('AppID', self._application_id)
        body.add_header('Context', str(context))

        message = SLPRequestMessage('INVITE',
                "MSNMSGR:" + self._peer.account,
                to = self._peer.account,
                frm = self._client.profile.account,
                branch = _generate_guid(),
                cseq = 0,
                call_id = self._call_id)

        message.body = body
        self._send_p2p_data(message)

    def close(self):
        body = SLPMessageBody(SLPContentType.SESSION_CLOSE)

        message = SLPRequestMessage('BYE',
                to = self._peer.account,
                frm = self._client.profile.account,
                branch = _generate_guid(),
                cseq = 0,
                call_id = self._call_id)
        message.body = body
        self._send_p2p_data(message)

    def _send_p2p_data(self, data_or_file):
        if isinstance(data_or_file, SLPMessage):
            session_id = 0
            data = str(data_or_file)
            total_size = len(data)
        else:
            session_id = self._session_id
            data = data_or_file
            total_size = None

        blob = MessageBlob(self._application_id,
                data, total_size, session_id)
        self._transport.send(blob)

    def _on_chunk_received(self, transport, chunk):
        pass

    def _on_blob_received(self, transport, blob):
        pass


class MSNObjectTransferSession(P2PSession):
    def __init__(self, client, peer, application_id):
        P2PSession.__init__(self, client, peer,
                EufGuid.MSN_OBJECT, application_id)

    def request(self, msn_object):
        context = base64.b64encode(msn_object + "\x00")
        return P2PSession.invite(self, context)

