import json
import urllib2

__author__ = 'Paul Durivage <pauldurivage@gmail.com'

class auth:
    """
    See Rackspace API for more information on the response:
        http://docs.rackspace.com/auth/api/v2.0/auth-client-devguide/content/Sample_Request_Response-d1e64.html
    """
    auth_dict = {"auth": {"RAX-KSKEY:apiKeyCredentials": {"username": None, "apiKey": None}}}
    apiEndpoint = {'us': 'https://identity.api.rackspacecloud.com/v2.0/tokens',
                   'uk': 'https://lon.identity.api.rackspacecloud.com/v2.0/tokens'}
    _serviceCatalog_ = {}

    def __init__(self, user, apikey, locale='us'):
        self.user = user
        self.apikey = apikey
        self.locale = locale
        self.doAuthRequest()

    def doAuthRequest(self):
        """
        Takes user and API key, builds request, executes request
        """
        auth_dict = self.auth_dict
        auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['username'] = self.user
        auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['apiKey'] = self.apikey
        request = self.buildAuthRequest(auth_dict)
        response = self.doRequest(request)
        if isinstance(response, file):
            self.setAuthResponse(response.read())
        elif isinstance(response, dict):
            raise RAXAPIException(response['error'])
        else:
            raise Exception('Unknown error occurred')

    def buildAuthRequest(self, auth_data):
        """
        Builds the request against the US indentity endpoint by default;
        returns request object
        """
        endpoint = (self.apiEndpoint[self.locale])
        request = urllib2.Request(endpoint)
        request.add_header('Content-type', 'application/json')
        request.add_header('Accept', 'application/json')
        request.add_data(json.dumps(auth_data))
        return request

    def doRequest(self, request):
        """
        Executes the request; returns a dict with the "error" key with the HTTP code as value;
        If successful, returns a response file-like obj.
        """
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as error:
            return {'error': error.code}
        else:
            if response:
                return response

    def setAuthResponse(self, response):
        """
        Converts JSON string to a dictionary and sets class attrib
        """
        self.setServiceCatalog(json.loads(response))

    def getServiceCatalog(self):
        """
        Returns full authentication response as a dictionary
        """
        return self._serviceCatalog_

    def setServiceCatalog(self, serviceCatalog):
        self._serviceCatalog_ = serviceCatalog

    def getOSCloudServers(self):
        return filter(lambda x: x['name'] == 'cloudServersOpenStack', self._serviceCatalog_['access']['serviceCatalog'])

    def getCloudFiles(self):
        pass

    def getCloudFilesCDN(self):
        pass

    def getCloudDB(self):
        pass

    def getCloudDNS(self):
        pass

    def getOldCloudServers(self):
        pass

    def getCloudMonitoring(self):
        pass

    def getUserInfo(self):
        pass

    def getToken(self):
        """
        Returns a dict in the form of {'expires': expiration, 'id': token}
        """
        return self._serviceCatalog_['access']['token']

class RAXAPIException(Exception):
    def __init__(self, errVal):
        self.errVal = errVal
    def __str__(self):
        return repr(self.errVal)
    def message(self):
        return repr('The server returned an error code: ' + repr(self.errVal))
