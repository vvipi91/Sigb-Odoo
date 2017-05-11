# -*- coding: utf-8 -*-
import xmlrpclib

class RestLogin(object):
    db = None
    url = None
    username = None
    password = None
    common = None
    uid = None

    def __init__(self, db, url, username, password):
        self.db = db
        self.url = url
        self.username = username
        self.password = password

    def validate_request(self):
        return xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url))

    def authenticate_user(self):

        self.common = self.validate_request()
        self.uid = self.common.authenticate(self.db, self.username, self.password, {})

        if (self.uid):
            return self.uid
        else:
            return "None"
