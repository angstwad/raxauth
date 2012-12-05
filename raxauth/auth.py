import json
import urllib2
from .exceptions import RAXAPIException

__author__ = 'Paul Durivage <pauldurivage@gmail.com>'

class Authenticate(object):
    __auth_dict = {"auth": {
                "RAX-KSKEY:apiKeyCredentials":
                    {"username": None,
                     "apiKey": None}}}
    __apiEndpoint = {'us': 'https://identity.api.rackspacecloud.com/v2.0/tokens',
                     'uk': 'https://lon.identity.api.rackspacecloud.com/v2.0/tokens'}

    def __init__(self, user, apikey, locale='us'):
        self.__user = user
        self.__apikey = apikey
        self.__locale = locale
        self.__doAuthRequest()

    def __doAuthRequest(self):
        """
        Takes user and API key, builds request, executes request
        """
        auth_dict = self.__auth_dict
        auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['username'] = self.__user
        auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['apiKey'] = self.__apikey
        request = self.__buildAuthRequest(auth_dict)
        response = self.__execRequest(request)
        if isinstance(response, urllib2.addinfourl):
            self.__setAuthResponse(response.read())
        elif isinstance(response, dict):
            raise RAXAPIException(response['error'])
        else:
            raise Exception('Unknown error occurred')

    def __buildAuthRequest(self, auth_data):
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

    def __execRequest(self, request):
        """
        Executes the request; returns a dict with the "error" key with the HTTP code as value;
        If successful, returns a response file-like obj.
        """
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as error:
            return {'error': 'Non-200 server response: ' + repr(error.code)}
        except urllib2.URLError as error:
            return {'error': 'Cannot contact remote host'}

        else:
            if response:
                return response

    def __setAuthResponse(self, response):
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

class auth(object):
    """
    See Rackspace API for more information on the response:
        http://docs.rackspace.com/auth/api/v2.0/auth-client-devguide/content/Sample_Request_Response-d1e64.html
    """
    def __init__(self, user, apikey, locale='us'):
        a = Authenticate(user, apikey, locale=locale)
        self.__serviceCatalog = a.getServiceCatalog()

    def getOSServerEndpoint(self, region=None, key='publicURL'):
        """
        Regions as of this writing are either "ORD", "DFW", or "LON".
        Returns a string public URL for the endpoint by default.  Will return the appropriate key if explicicity defined.
        If no region is defined, the user's default region endpoint is pulled from the service catalog and returns that public URL.
        If region is all, return the whole thing.
        """
        region = self.__toUpper(region)
        selection = filter(lambda x: x['name'] == 'cloudServersOpenStack', self.__serviceCatalog['access']['serviceCatalog'])[0]
        if region is None:
            regionDict = filter(lambda x: x['region'] == self.__serviceCatalog['access']['user']['RAX-AUTH:defaultRegion'],
                selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'DFW':
            regionDict = filter(lambda x: x['region'] == 'DFW', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ORD':
            regionDict = filter(lambda x: x['region'] == 'ORD', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ALL':
            return selection

    def getServerEndpoint(self, region=None, key='publicURL'):
        """
        If region is 'all', it returns the value specified by the key, by default
        returning the public URL of the endpoint as a string.
        """
        region = self.__toUpper(region)
        selection = filter(lambda x: x['name'] == 'cloudServers', self.__serviceCatalog['access']['serviceCatalog'])[0]
        if region == 'ALL':
            return selection
        elif region is None:
            return selection['endpoints'][0][key]

    def getFilesEndpoint(self, region=None, key='publicURL'):
        """
        If region is the none, return default datacenter 'key' value;
        If region is DFW or ORD, return value of 'key' for that endpoint.
        If region is all, the full Cloud Files endpoint dictionary is returned.
        """
        region = self.__toUpper(region)
        selection = filter(lambda x: x['name'] == 'cloudFiles', self.__serviceCatalog['access']['serviceCatalog'])[0]
        if region is None:
            regionDict = filter(lambda x: x['region'] == self.__serviceCatalog['access']['user']['RAX-AUTH:defaultRegion'],
                selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'DFW':
            regionDict = filter(lambda x: x['region'] == 'DFW', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ORD':
            regionDict = filter(lambda x: x['region'] == 'ORD', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ALL':
            return selection

    def getLoadBalEndpoint(self, region=None, key='publicURL'):
        """
        If region is the none, return default datacenter 'key' value;
        If region is DFW or ORD, return value of 'key' for that endpoint.
        If region is all, the full Cloud Load Balancer endpoint dictionary is returned.
        """
        selection = filter(lambda x: x['name'] == 'cloudLoadBalancers', self.__serviceCatalog['access']['serviceCatalog'])[0]
        if region is None:
            regionDict = filter(lambda x: x['region'] == self.__serviceCatalog['access']['user']['RAX-AUTH:defaultRegion'],
                selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'DFW':
            regionDict = filter(lambda x: x['region'] == 'DFW', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ORD':
            regionDict = filter(lambda x: x['region'] == 'ORD', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ALL':
            return selection

    def getFilesCDNEndpoint(self, region=None, key='publicURL'):
        """
        If region is the none, return default datacenter 'key' value;
        If region is DFW or ORD, return value of 'key' for that endpoint.
        If region is all, the full Cloud Files CDN endpoint dictionary is returned.
        """
        selection = filter(lambda x: x['name'] == 'cloudFilesCDN', self.__serviceCatalog['access']['serviceCatalog'])[0]
        if region is None:
            regionDict = filter(lambda x: x['region'] == self.__serviceCatalog['access']['user']['RAX-AUTH:defaultRegion'],
                selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'DFW':
            regionDict = filter(lambda x: x['region'] == 'DFW', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ORD':
            regionDict = filter(lambda x: x['region'] == 'ORD', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ALL':
            return selection

    def getDBEndpoint(self, region=None, key='publicURL'):
        """
        If region is the none, return default datacenter 'key' value;
        If region is DFW or ORD, return value of 'key' for that endpoint.
        If region is all, the full Cloud Databases endpoint dictionary is returned.
        """
        selection = filter(lambda x: x['name'] == 'cloudDatabases', self.__serviceCatalog['access']['serviceCatalog'])[0]
        if region is None:
            regionDict = filter(lambda x: x['region'] == self.__serviceCatalog['access']['user']['RAX-AUTH:defaultRegion'],
                selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'DFW':
            regionDict = filter(lambda x: x['region'] == 'DFW', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ORD':
            regionDict = filter(lambda x: x['region'] == 'ORD', selection['endpoints'])[0]
            return regionDict[key]
        elif region == 'ALL':
            return selection

    def getCloudDNS(self):
        """ Feature complete; Only returns on endpoint. """
        return filter(lambda x: x['name'] == 'cloudDNS', self.__serviceCatalog['access']['serviceCatalog'])[0]['endpoints'][0]['publicURL']

    def getCloudMonitoring(self):
        """ Feature complete; Only returns on endpoint. """
        return filter(lambda x: x['name'] == 'cloudMonitoring', self.__serviceCatalog['access']['serviceCatalog'])[0]['endpoints'][0]['publicURL']

    def getUserInfo(self):
        """
        Returns dict of user rights and information
        """
        return self.__serviceCatalog['access']['user']

    def getToken(self):
        """
        Returns a dict in the form of {'expires': expiration, 'id': token}
        """
        return {'expires': self.__serviceCatalog['access']['token']['expires'],
                'id': self.__serviceCatalog['access']['token']['id']}

    def __toUpper(self, word):
        try:
            return word.upper()
        except AttributeError:
            return None