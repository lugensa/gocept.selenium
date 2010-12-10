#############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################


class SimpleApp(object):

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        statuscode = '404 Not Found'
        body = 'Not Found'
        headers = []
        if path == '/':
            statuscode = '200 OK'
            headers.append(('Content-Type', 'text/html'))
            body = '''
              <html>
              <head>
                <script src="colors.js"></script>
              </head>
              <body>
                <p id="foo">Testing...</p>
              </body>
              </html>'''
        elif path == '/colors.js':
            statuscode = '200 OK'
            headers.append(('Content-Type', 'text/javascript'))
            body = '''\
var hello = function hello () {
    document.getElementById('foo').innerHTML = 'Hello from javascript';
};
window.onload = hello;'''
        start_response(statuscode, headers)
        return body


class SimpleApp2(object):

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return '<html><head></head><body>simple</body></html>'
