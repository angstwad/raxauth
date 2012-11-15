import json
import urllib2

class auth:
    auth_dict = {"auth": {"RAX-KSKEY:apiKeyCredentials": {"username": None, "apiKey": None}}}

    apiEndpoint = {'us': 'https://identity.api.rackspacecloud.com/v2.0/',
                   'uk': 'https://lon.identity.api.rackspacecloud.com/v2.0/'}

    def doAuthRequest(self, user, apikey):
        """
        Takes user and API key, builds request, executes request, and returns
        a dict with the JSON auth response.  See Rackspace API for more information
        on the response:
        http://docs.rackspace.com/auth/api/v2.0/auth-client-devguide/content/Sample_Request_Response-d1e64.html
        """
        auth_dict = self.auth_dict
        auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['username'] = user
        auth_dict['auth']['RAX-KSKEY:apiKeyCredentials']['apiKey'] = apikey
        # Call build auth request with our JSON requst data in auth_dict
        request = self.buildAuthRequest(auth_dict)
        # Take our request and execute it against US endpoint
        response = self.doRequest(request)
        # Return the JSON response as a dict
        return self.parseAuthResponse(response)

    def buildAuthRequest(self, auth_data, Locale='us'):
        """
        Builds the request against the US indentity endpoint by default;
        returns request object
        """
        endpoint = (self.apiEndpoint[Locale] + 'tokens')
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

    def parseAuthResponse(self, response):
        return json.loads(response.read())



