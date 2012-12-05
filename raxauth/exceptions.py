__author__ = 'Paul Durivage <paul.durivage@rackspace.com>'

class RAXAPIException(Exception):
    def __init__(self, errVal):
        self.errVal = errVal
    def __str__(self):
        return repr(self.errVal)
    def message(self):
        return repr('The server returned an error code: ' + repr(self.errVal))