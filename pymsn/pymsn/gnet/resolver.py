# -*- coding: utf-8 -*-
#
# Copyright (C) 2006  Ali Sabil <ali.sabil@gmail.com>
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

"""GNet dns resolver"""

import socket

import adns
import gobject

__all__ = ['HostnameResolver']

class HostnameResponse(object):
    def __init__(self, response):
        self._response = response

    @property
    def status(self):
        return self._response[0]

    @property
    def cname(self):
        return self._response[1]

    @property
    def expires(self):
        return self._response[2]

    @property
    def answer(self):
        return self._response[3]

    def __repr__(self):
        return repr(self._response)

class HostnameResolver(object):
    def __init__(self):
        self._c = adns.init(adns.iflags.noautosys)
        self._queries = {}

    def query(self, host, callback):
        if self._is_ip(host):
            self._emit_response(callback, (0, None, 0, ((2, host),)))
            return
    
        query = self._c.submit(host, adns.rr.ADDR)
        self._queries[query] = host, callback
        if len(self._queries) == 1:
            gobject.timeout_add(10, self._process_queries)

    def _is_ip(self, address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, address)
            except socket.error:
                return False
            return True
        return True

    def _process_queries(self):
        for query in self._c.completed(0):
            response = query.check()
            qname, callback = self._queries[query]
            del self._queries[query]
            self._emit_response(callback, response)
        return len(self._queries) > 0

    def _emit_response(self, callback, response):
        callback[0](HostnameResponse(response), *callback[1:])
        return False


if __name__ == "__main__":
    mainloop = gobject.MainLoop(is_running=True)
    def print_throbber():
        print "*"
        return True

    def hostname_resolved(result):
        print result
        mainloop.quit()

    def resolve_hostname(resolver, host):
        print "Resolving"
        resolver.query(host, (hostname_resolved,))
        return False

    resolver = HostnameResolver()
    
    gobject.timeout_add(10, print_throbber)
    gobject.timeout_add(100, resolve_hostname, resolver, 'www.google.com')
    #gobject.timeout_add(100, resolve_hostname, resolver, '209.85.129.104')
    
    mainloop.run()

