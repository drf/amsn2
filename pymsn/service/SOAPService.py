# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2005-2007 Ali Sabil <ali.sabil@gmail.com>
# Copyright (C) 2007 Johann Prieur <johann.prieur@gmail.com>
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

import description
from SOAPUtils import *

import pymsn.gnet.protocol
import pymsn.util.ElementTree as ElementTree
import pymsn.util.StringIO as StringIO
import re
import logging

__all__ = ['SOAPService', 'SOAPResponse']

logger = logging.getLogger('Service')

def url_split(url, default_scheme='http'):
    from urlparse import urlsplit, urlunsplit
    if "://" not in url: # fix a bug in urlsplit
        url = default_scheme + "://" + url
    protocol, host, path, query, fragment = urlsplit(url)
    if path == "": path = "/"
    try:
        host, port = host.rsplit(":", 1)
        port = int(port)
    except:
        port = None
    resource = urlunsplit(('', '', path, query, fragment))
    return protocol, host, port, resource

def compress_xml(xml_string):
    space_regex = [(re.compile('>\s+<'), '><'),
        (re.compile('>\s+'), '>'),
        (re.compile('\s+<'), '<')]

    for regex, replacement in space_regex:
        xml_string = regex.sub(replacement, xml_string)
    return xml_string

soap_template = """<?xml version='1.0' encoding='utf-8'?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Header>
        %s
    </soap:Header>
    <soap:Body>
        %s
    </soap:Body>
</soap:Envelope>"""

class SOAPResponse(ElementTree.XMLResponse):
    NS_SHORTHANDS = {'soap' : XMLNS.SOAP.ENVELOPE,
            "xmlenc" : XMLNS.ENCRYPTION.BASE,
            "wsse" : XMLNS.WS.SECEXT,
            "wst" : XMLNS.WS.TRUST,
            "wsa" : XMLNS.WS.ADDRESSING,
            "wsp" : XMLNS.WS.POLICY,
            "wsi" : XMLNS.WS.ISSUE,
            "wsu" : XMLNS.WS.UTILITY,
            "ps" : XMLNS.MICROSOFT.PASSPORT,
            "ab" : XMLNS.MICROSOFT.LIVE.ADDRESSBOOK,
            "st" : XMLNS.MICROSOFT.LIVE.STORAGE,
            "oim" : XMLNS.MICROSOFT.LIVE.OIM,
            "rsi" : XMLNS.MICROSOFT.LIVE.RSI }

    def __init__(self, soap_data):
        ElementTree.XMLResponse.__init__(self, soap_data, self.NS_SHORTHANDS)
        try:
            self.header = self.tree.find("./soap:Header")
            self.body = self.tree.find("./soap:Body")
            self.fault = self.body.find("./soap:Fault")
        except:
            self.tree = None
            self.header = None
            self.body = None
            self.fault = None
            logger.warning("SOAPResponse: Invalid xml+soap data")

    def is_fault(self):
        return self.fault is not None

    def is_valid(self):
        return ((self.header is not None) or \
                (self.fault is not None) or \
                (self.body is not None)) \
            and self.tree is not None

    def _parse(self, data):
        events = ("start", "end", "start-ns", "end-ns")
        ns = []
        data = StringIO.StringIO(data)
        context = ElementTree.iterparse(data, events=events)
        for event, elem in context:
            if event == "start-ns":
                ns.append(elem)
            elif event == "end-ns":
                ns.pop()
            elif event == "start":
                elem.set("(xmlns)", tuple(ns))
        data.close()
        return context.root

class SOAPService(object):

    def __init__(self, name, proxies=None):
        self._name = name
        self._service = getattr(description, self._name)
        self._active_transports = {}
        self._proxies = proxies or {}

    def _send_request(self, name, url, soap_header, soap_body, soap_action,
            callback, errback=None, transport_headers={}, user_data=None):
        
        scheme, host, port, resource = url_split(url)
        http_headers = transport_headers.copy()
        if soap_action is not None:
            http_headers["SOAPAction"] = str(soap_action)
        http_headers["Content-Type"] = "text/xml; charset=utf-8"
        http_headers["Cache-Control"] = "no-cache"
        if "Accept" not in http_headers:
            http_headers["Accept"] = "text/*"
        http_headers["Proxy-Connection"] = "Keep-Alive"
        http_headers["Connection"] = "Keep-Alive"

        request = compress_xml(soap_template % (soap_header, soap_body))

        transport = self._get_transport(name, scheme, host, port,
                callback, errback, user_data)
        transport.request(resource, http_headers, request, 'POST')

    def _response_handler(self, transport, http_response):
        logger.debug("<<< " + str(http_response))
        soap_response = SOAPResponse(http_response.body)
        request_id, callback, errback, user_data = self._unref_transport(transport)

        if not soap_response.is_valid():
            logger.warning("Invalid SOAP Response")
            return #FIXME: propagate the error up

        if not soap_response.is_fault():
            handler = getattr(self,
                    "_Handle" + request_id + "Response",
                    None)
            method = getattr(self._service, request_id)
            response = method.process_response(soap_response)
            
            if handler is not None:
                handler(callback, errback, response, user_data)
            else:
                self._HandleUnhandledResponse(request_id, callback, errback,
                        response, user_data)
        else:
            self._HandleSOAPFault(request_id, callback, errback, soap_response,
                    user_data)

    def _request_handler(self, transport, http_request):
        logger.debug(">>> " + str(http_request))

    def _error_handler(self, transport, error):
        logger.warning("Transport Error :" + str(error))
        request_id, callback, errback = self._unref_transport(transport)
        return request_id, callback, errback #FIXME: do something sensible here

    # Handlers
    def _HandleSOAPFault(self, request_id, callback, errback,
            soap_response, user_data):
        logger.warning("Unhandled SOAPFault to %s" % request_id)

    def _HandleUnhandledResponse(self, request_id, callback, errback,
            response, user_data):
        logger.warning("Unhandled Response to %s" % request_id)

    # Transport management
    def _get_transport(self, request_id, scheme, host, port,
            callback, errback, user_data):
        key = (scheme, host, port)
        if key in self._active_transports:
            trans = self._active_transports[key]
            transport = trans[0]
            trans[1].append((request_id, callback, errback, user_data))
        else:
            proxy = self._proxies.get(scheme, None)
            transport = pymsn.gnet.protocol.ProtocolFactory(scheme,
                    host, port, proxy=proxy)
            handler_id = [transport.connect("response-received",
                    self._response_handler),
                transport.connect("request-sent", self._request_handler),
                transport.connect("error", self._error_handler)]

            trans = [transport, [(request_id, callback, errback, user_data)], handler_id]
            self._active_transports[key] = trans
        return transport

    def _unref_transport(self, transport):
        for key, trans in self._active_transports.iteritems():
            if trans[0] == transport:
                response = trans[1].pop(0)
                
                if len(trans[1]) != 0:
                    return response

                for handle in trans[2]:
                    transport.disconnect(handle)
                del self._active_transports[key]
                return response
        return None

