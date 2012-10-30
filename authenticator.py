import json
import urllib2

class auth:
    auth_dict = {"auth": {"RAX-KSKEY:apiKeyCredentials": {"username": None, "apiKey": None}}}

    apiEndpoint = {'us': 'https://identity.api.rackspacecloud.com/v2.0/',
                   'uk': 'https://lon.identity.api.rackspacecloud.com/v2.0/'}

    def __init__(self):
        pass

    def doAuthRequest(self, user, apikey):
        self.auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['username'] = user
        self.auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['apiKey'] = apikey
        # Call build auth request with our JSON requst data in auth_dict
        request = self.buildAuthRequest(self, self.auth_dict)
        response = self.doRequest(request)


    def buildAuthRequest(self, auth_data, Locale='us'):
        request = urllib2.Request(self.apiEndpoint[Locale]+'tokens')
        request.add_header('Content-type', 'application/json')
        request.add_header('Accept', 'application/json')
        request.add_data(json.dumps(auth_data))
        return request

    def doRequest(self, request):
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as error:
            return {'error': error.code}
        if response:
            return response

    def parseAuthResponse(self, response):
        return json.loads(response.read())



