import json
import urllib2

__author__ = 'Paul Durivage <pauldurivage@gmail.com>'

class auth(object):
    """
    See Rackspace API for more information on the response:
        http://docs.rackspace.com/auth/api/v2.0/auth-client-devguide/content/Sample_Request_Response-d1e64.html
    """
    __auth_dict = {"auth": {"RAX-KSKEY:apiKeyCredentials": {"username": None, "apiKey": None}}}
    __apiEndpoint = {'us': 'https://identity.api.rackspacecloud.com/v2.0/tokens',
                   'uk': 'https://lon.identity.api.rackspacecloud.com/v2.0/tokens'}
    __serviceCatalog = {}

    def __init__(self, user, apikey, locale='us'):
        self.__user = user
        self.__apikey = apikey
        self.__locale = locale
        self.doAuthRequest()

    def doAuthRequest(self):
        """
        Takes user and API key, builds request, executes request
        """
        auth_dict = self.__auth_dict
        auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['username'] = self.__user
        auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['apiKey'] = self.__apikey
        request = self.buildAuthRequest(auth_dict)
        response = self.doRequest(request)
        if isinstance(response, urllib2.addinfourl):
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
        endpoint = (self.__apiEndpoint[self.__locale])
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
        Returns full service catalog response as a dictionary
        """
        return self.__serviceCatalog

    def setServiceCatalog(self, serviceCatalog):
        self.__serviceCatalog = serviceCatalog

    def getOSCloudServers(self):
        return filter(lambda x: x['name'] == 'cloudServersOpenStack', self.__serviceCatalog['access']['serviceCatalog'])

    def getCloudFiles(self):
        return filter(lambda x: x['name'] == 'cloudFiles', self.__serviceCatalog['access']['serviceCatalog'])

    def getCloudLB(self):
        self.__serviceCatalog
        return filter(lambda x: x['name'] == 'cloudLoadBalancers', self.__serviceCatalog['access']['serviceCatalog'])

    def getCloudFilesCDN(self):
        return filter(lambda x: x['name'] == 'cloudFilesCDN', self.__serviceCatalog['access']['serviceCatalog'])

    def getCloudDB(self):
        return filter(lambda x: x['name'] == 'cloudDatabases', self.__serviceCatalog['access']['serviceCatalog'])

    def getCloudDNS(self):
        return filter(lambda x: x['name'] == 'cloudDNS', self.__serviceCatalog['access']['serviceCatalog'])

    def getOldCloudServers(self):
        return filter(lambda x: x['name'] == 'cloudServers', self.__serviceCatalog['access']['serviceCatalog'])

    def getCloudMonitoring(self):
        return filter(lambda x: x['name'] == 'cloudMonitoring', self.__serviceCatalog['access']['serviceCatalog'])

    def getUserInfo(self):
        """
        Returns dict of user rights and information
        """
        return self.__serviceCatalog['access']['user']

    def getToken(self):
        """
        Returns a dict in the form of {'expires': expiration, 'id': token}
        """
        return self.__serviceCatalog['access']['token']

class RAXAPIException(Exception):
    def __init__(self, errVal):
        self.errVal = errVal
    def __str__(self):
        return repr(self.errVal)
    def message(self):
        return repr('The server returned an error code: ' + repr(self.errVal))