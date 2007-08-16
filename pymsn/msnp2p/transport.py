# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2007 Ali Sabil <asabil@gmail.com>
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

import pymsn.util.StringIO as StringIO
from pymsn.switchboard_manager import SwitchboardClient
from pymsn.msnp.message import MessageAcknowledgement

import struct
import gobject
import random
import logging
from copy import copy

__all__ = ['MessageBlob', 'SwitchboardP2PTransport']

MAX_INT32 = 2147483647

logger = logging.getLogger('msnp2p:transport')

def _generate_id(max=MAX_INT32):
    """
    Returns a random ID.

        @return: a random integer between 1000 and sys.maxint
        @rtype: integer
    """
    return random.randint(1000, max)

_previous_chunk_id = _generate_id(MAX_INT32 - 1)
def _chunk_id():
    global _previous_chunk_id
    _previous_chunk_id += 1
    if _previous_chunk_id == MAX_INT32:
        _previous_chunk_id = 1
    return _previous_chunk_id

class TLPHeader(object):
    SIZE = 48

    def __init__(self, *header):
        header = list(header)
        header[len(header):] = [0] * (9 - len(header))

        self.session_id = header[0]
        self.blob_id = header[1]
        self.blob_offset = header[2]
        self.blob_size = header[3]
        self.chunk_size = header[4]
        self.flags = header[5]
        self.dw1 = header[6]
        self.dw2 = header[7]
        self.qw1 = header[8]

    def __str__(self):
        return struct.pack("<LLQQLLLLQ", self.session_id,
                self.blob_id,
                self.blob_offset,
                self.blob_size,
                self.chunk_size,
                self.flags,
                self.dw1,
                self.dw2,
                self.qw1)
    
    @staticmethod
    def parse(header_data):
        header = struct.unpack("<LLQQLLLLQ", header_data[:48])
        session_id = header[0]
        blob_id = header[1]
        blob_offset = header[2]
        blob_size = header[3]
        chunk_size = header[4]
        flags = header[5]
        dw1 = header[6]
        dw2 = header[7]
        qw1 = header[8]
        return TLPHeader(session_id, blob_id, blob_offset, blob_size,
                chunk_size, flags, dw1, dw2, qw1)


class TLPFlag(object):
    NAK = 0x1
    ACK = 0x2
    RAK = 0x4
    RST = 0x8
    FILE = 0x10
    EACH = 0x20
    CAN = 0x40
    ERR = 0x80
    KEY = 0x100
    CRYPT = 0x200


class MessageChunk(object):
    def __init__(self, header, body):
        self.header = header
        self.body = body
        self.application_id = 0

    def __str__(self):
        return str(self.header) + str(self.body)

    def is_control_chunk(self):
        return self.header.flags & 0xFFFFFFCF

    def is_ack_chunk(self):
        return self.header.flags & (TLPFlag.NAK | TLPFlag.ACK)

    def require_ack(self):
        if self.is_ack_chunk():
            return False
        if self.header.flags & TLPFlag.EACH:
            return True
        current_size = self.header.chunk_size + self.header.blob_offset
        if current_size == self.header.blob_size:
            return True
        return False

    @staticmethod
    def parse(data):
        header = TLPHeader.parse(data[:48])
        body = data[48:]
        return MessageChunk(header, body)


class MessageBlob(object):
    def __init__(self, application_id, data, total_size=None,
            session_id=None, blob_id=None):
        if data is not None:
            if isinstance(data, str):
                data = StringIO.StringIO(data)

            if total_size is None:
                self.data.seek(0, 2) # relative to the end
                total_size = self.data.tell()
                self.data.seek(0, 0)
        else:
            total_size = 0

        self.data = data
        self.total_size = total_size
        self.application_id = application_id
        if session_id is None:
            session_id = _generate_id()
        self.session_id = session_id
        self.id = blob_id or _generate_id()

    def __del__(self):
        if self.data is not None:
            self.data.close()

    def __getattr__(self, name):
        return getattr(self.data, name)
    
    @property
    def transferred(self):
        if self.data is None:
            return 0
        return self.data.tell()

    def is_complete(self):
        return self.transferred == self.total_size

    def is_control_blob(self):
        return False

    def get_chunk(self, max_size):
        blob_offset = self.transferred

        if self.data is not None:
            data = self.data.read(max_size - TLPHeader.SIZE)
            assert len(data) > 0, "Trying to read more data than available"
        else:
            data = ""
        
        header = TLPHeader()
        header.session_id = self.session_id
        header.blob_id = self.id
        header.blob_offset = blob_offset
        header.blob_size = self.total_size
        header.chunk_size = len(data)
        header.dw1 = _chunk_id()

        chunk = MessageChunk(header, data)
        chunk.application_id = self.application_id
        return chunk

    def append_chunk(self, chunk):
        assert self.data is not None, "Trying to write to a Read Only blob"
        assert self.session_id == chunk.header.session_id, "Trying to append a chunk to the wrong blob"
        assert self.id == chunk.header.blob_id, "Trying to append a chunk to the wrong blob"
        self.data.seek(chunk.header.blob_offset, 0)
        self.data.write(chunk.body)


class ControlBlob(MessageBlob):
    def __init__(self, session_id, flags, dw1=0, dw2=0, qw1=0):
        MessageBlob.__init__(self, 0, None)
        header = TLPHeader(session_id, self.id, 0, 0, 0,
                flags, dw1, dw2, qw1)
        self.chunk = MessageChunk(header, "")

    def get_chunk(self, max_size):
        return self.chunk
    
    def is_control_blob(self):
        return True


class BaseP2PTransport(gobject.GObject):
    __gsignals__ = {
            "chunk-received": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),

            "chunk-sent": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),

            "blob-received": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,))
            }
    
    def __init__(self, client, name, peer):
        gobject.GObject.__init__(self)
        self._client = client
        self._name = name
        self._peer = peer
        self._reset()

    @property
    def name(self):
        return self._name
    
    @property
    def peer(self):
        return self._peer
    
    @property
    def rating(self):
        raise NotImplementedError
    
    @property
    def max_chunk_size(self):
        raise NotImplementedError

    def send(self, blob, callback=None, errback=None):
        if blob.is_control_blob():
            self._control_blob_queue.append(blob)
        else:
            self._data_blob_queue.append(blob)
        self._process_send_queues()

    def register_writable_blob(self, blob):
        if blob.session_id in self._writable_blobs:
            logger.warning("registering already registered blob "\
                    "with session_id=" str(session_id))
            return
        self._writable_blobs[blob.session_id] = blob

    def _send_chunk(self, chunk):
        raise NotImplementedError

    # Helper methods
    def _reset(self):
        self._writable_blobs = {}
        self._control_blob_queue = []
        self._data_blob_queue = []
        self._pending_ack = {} # blob_id : [blob_offset1, blob_offset2 ...]

    def _add_pending_ack(self, blob_id, chunk_id=0):
        if blob_id not in self._pending_ack:
            self._pending_ack[blob_id] = set()
        self._pending_ack[blob_id].add(chunk_id)

    def _del_pending_ack(self, blob_id, chunk_id=0):
        if blob_id not in self._pending_ack:
            return
        self._pending_ack[blob_id].discard(chunk_id)

        if len(self._pending_ack[blob_id]) == 0:
            del self._pending_ack[blob_id]

    def _on_chunk_received(self, chunk):
        if chunk.require_ack():
            self._send_ack(chunk)

        if chunk.header.flags & TLPFlag.ACK:
            self._del_pending_ack(chunk.header.dw1, chunk.header.dw2)

        #FIXME: handle all the other flags

        if not chunk.is_control_chunk():
            self.emit("chunk-received", chunk)
            session_id = chunk.header.session_id
            if session_id == 0:
                return

            if session_id in self._writable_blobs:
                blob = self._writable_blobs[session_id]

                if chunk.header.blob_offset == 0:
                    blob.id = chunk.header.blob_id

                blob.append_chunk(chunk)
                if blob.is_complete():
                    self.emit("blob-received", blob)
                    del self._writable_blobs[session_id]

        self._process_send_queues()

    def _on_chunk_sent(self, chunk):
        self.emit("chunk-sent", chunk)
        self._process_send_queues()

    def _process_send_queues(self):
        if len(self._control_blob_queue) > 0:
            queue = self._control_blob_queue
        elif len(self._data_blob_queue) > 0:
            queue = self._data_blob_queue
        else:
            return

        blob = queue[0]
        chunk = blob.get_chunk(self.max_chunk_size)
        if blob.is_complete():
            queue.pop(0) # FIXME: we should keep it in the queue until we receive the ACK

        if chunk.require_ack() :
            self._add_pending_ack(chunk.header.blob_id, chunk.header.dw1)
        self._send_chunk(chunk)

    def _send_ack(self, received_chunk):
        flags = received_chunk.header.flags

        flags = TLPFlag.ACK
        if received_chunk.header.flags & TLPFlag.RAK:
            flags |= TLPFlag.RAK

        ack_blob = ControlBlob(0, flags, 
                dw1 = received_chunk.header.blob_id,
                dw2 = received_chunk.header.dw1,
                qw1 = received_chunk.header.blob_size)

        self.send(ack_blob)

gobject.type_register(BaseP2PTransport) 

class SwitchboardP2PTransport(BaseP2PTransport, SwitchboardClient):
    def __init__(self, client, peer):
        BaseP2PTransport.__init__(self, client, "switchboard", peer)
        SwitchboardClient.__init__(self, client, (peer,))

    @staticmethod
    def _can_handle_message(message, switchboard_client=None):
        content_type = message.content_type[0]
        return content_type == 'application/x-msnmsgrp2p'

    @property
    def rating(self):
        return 0
    
    @property
    def max_chunk_size(self):
        return 1250 # length of the chunk including the header but not the footer

    def _send_chunk(self, chunk):
        headers = {'P2P-Dest': self.peer.account}
        content_type = 'application/x-msnmsgrp2p'
        body = str(chunk) + struct.pack('>L', chunk.application_id)
        self._send_message(content_type, body, headers, MessageAcknowledgement.MSNC)

    def _on_message_received(self, message):
        chunk = MessageChunk.parse(message.body[:-4])
        chunk.application_id = struct.unpack('>L', message.body[-4:])[0]
        self._on_chunk_received(chunk)

    def _on_message_sent(self, message):
        chunk = MessageChunk.parse(message.body[:-4])
        chunk.application_id = struct.unpack('>L', message.body[-4:])[0]
        self._on_chunk_sent(chunk)

