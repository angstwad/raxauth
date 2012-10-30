#!/usr/bin/env python

import json
import urllib2
from sys import exit

__author__ = 'paul durivage'

username = ''
apikey = ''
auth_url = "https://identity.api.rackspacecloud.com/v2.0/tokens"

def main():
    print 'Authenticating for user "%s"...' % username
    #request =
    #response =
    #jsonAuthObj =
    authToken = parseAuthResponse(makeRequest(createRequest(username, apikey)))

    print '\nAPI Token: %(token)s\nExpires: %(exp)s' % returnAuthToken(authToken)

    #f = open('~/.apitoken', )

def createRequest(usr, api):
    """
    This function authenticates against the US Rackspace API and returns the request,
    a serialized JSON string.
    """
    auth_dict = {"auth": {"RAX-KSKEY:apiKeyCredentials": {"username": usr, "apiKey": api}}}

    request = urllib2.Request(auth_url)
    request.add_header('Content-type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.add_data(json.dumps(auth_dict))

    return request

def makeRequest(request):
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:

        print '\nResponse Code:', e.getcode(), '\n'
        print e.info()
        exit(1)

    if response:
        print "Success!"
        return response

def parseAuthResponse(response):
    """
    This function deserializes the JSON response string into a Python dict.
    """
    return json.loads(response.read())

def returnAuthToken(jsonAuthObj):
    """
    This function returns the Auth Token String from the Auth object.
    """
    return {'token': jsonAuthObj['access']['token']['id'], 'exp': jsonAuthObj['access']['token']['expires'] }

def cacheData(data):
    pass

def getCacheData():
    pass

if __name__ == '__main__':
    main()